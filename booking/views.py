from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from .models import Booking
from .serializers import BookingSerializer
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Booking
from .utils import create_qr_code, create_pdf


class BookingListCreateAPIView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
class BookingRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

def booking_detail(request, id):
    booking = get_object_or_404(Booking, id=id)
    qr_data = f"http://{request.get_host()}/booking/list/{booking.id}/"
    print(qr_data)  # Konsolda tekshirish uchun chop eting
    qr_img = create_qr_code(qr_data)
    
    pdf_buffer = create_pdf(booking, qr_img)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{booking.id}.pdf"'
    response.write(pdf_buffer.getvalue())
    return response