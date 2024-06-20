from django.db import models
from common.models import BaseModel
from tour.models import Tour
from django.contrib.auth import get_user_model

User = get_user_model()

class Booking(BaseModel):
    STATUS = (
        (1,'process'),
        (2,'confirmed'),
        (3,'cancel'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    seats_count = models.PositiveIntegerField(default=0)
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=9)
    phone_number = models.CharField(max_length=255)
    comment = models.CharField(max_length=500)