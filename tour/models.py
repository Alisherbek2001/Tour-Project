from django.db import models
from common.models import BaseModel
from account.models import Agency

from django.contrib.auth import get_user_model

User = get_user_model()

class Category(BaseModel):
    name = models.CharField(max_length=255) 
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
 
class Tour(BaseModel):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    category = models.ManyToManyField(Category)
    agency = models.ForeignKey(Agency,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    seats = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Tour"
        verbose_name_plural = "Tours"
        
        
class TourService(BaseModel):
    name = models.CharField(max_length=255)
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
class Image(BaseModel):
    image = models.ImageField(upload_to="image/")
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE)
    
class Video(BaseModel):
    video = models.FileField(upload_to='video/')
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE)

class Feedback(BaseModel):
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self) -> str:
        return self.tour.name
    
    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        
        
    