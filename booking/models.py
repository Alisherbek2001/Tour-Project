from django.db import models
from common.models import BaseModel
from tour.models import Tour
from django.contrib.auth import get_user_model

User = get_user_model()

class Booking(BaseModel):
    STATUS = (
        ('process','process'),
        ('confirmed','confirmed'),
        ('cancel','cancel'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    seats_count = models.PositiveIntegerField(default=0)
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS,max_length=9)
    phone_number = models.CharField(max_length=255)
    comment = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.id} {self.user.first_name} {self.user.last_name} - {self.tour.name}"
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'