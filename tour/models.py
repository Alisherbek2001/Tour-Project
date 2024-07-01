from django.db import models
from common.models import BaseModel
from account.models import Agency
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


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
    discount = models.IntegerField(default=0)
    seats = models.PositiveIntegerField(default=0)
    
    def add_or_update_rating(self, user, rating):
        if rating <= 0 or rating >= 5:
            raise ValidationError("The rating ranges from 0 to 5")
        
        tour_rating, created = TourRating.objects.update_or_create(
            tour=self,
            user=user,
            defaults={'rating': rating}
        )
        return tour_rating

    @property
    def average_rating(self):
        return self.tourrating_set.aggregate(Avg('rating'))['rating__avg']
    
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
    is_approved =  models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.tour.name
    
    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        
        
class TourRating(BaseModel):
    rating = models.PositiveSmallIntegerField(default=5)
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.id} {self.tour.name} {self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        unique_together = ('tour', 'user')