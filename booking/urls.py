from django.urls import path
from .views import *

urlpatterns = [
    path('',BookingListCreateAPIView.as_view()),
    path('<int:pk>/',BookingRetrieveUpdateDestroyAPIView.as_view()),
    path('list/<int:pk>/',BookingListAPIView.as_view()),
    path('pdf/<int:id>/', booking_detail, name='booking-pdf-detail'),
]