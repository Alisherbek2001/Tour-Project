import qrcode
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def create_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    return img

def create_pdf(booking, qr_image):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Booking ID: {booking.id}")
    c.drawString(100, 730, f"User: {booking.user.email}")
    c.drawString(100, 710, f"Tour: {booking.tour.name}")
    c.drawString(100, 690, f"Seats Count: {booking.seats_count}")
    c.drawString(100, 670, f"Status: {booking.get_status_display()}")
    c.drawString(100, 650, f"Phone Number: {booking.phone_number}")
    c.drawString(100, 630, f"Comment: {booking.comment}")

    # QR kodni vaqtinchalik faylga saqlash
    temp_buffer = BytesIO()
    qr_image.save(temp_buffer, format="PNG")
    temp_buffer.seek(0)
    qr_image_reader = ImageReader(temp_buffer)

    # QR kodni PDF ga qo'shish
    c.drawImage(qr_image_reader, 400, 700, 100, 100)
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer
