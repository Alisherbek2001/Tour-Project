from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.db.models import Avg


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    email = models.EmailField(_("email adress"), unique=True)
    phone = models.CharField(_("phone number"), max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_partner = models.BooleanField(default=False)
    image = models.ImageField(upload_to='User_Image/',null=True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    
class Agency(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='agency_image',null=True,blank=True)
    
    @property
    def rating(self):
        from tour.models import TourRating
        return TourRating.objects.filter(tour__agency=self).aggregate(Avg('rating'))['rating__avg']
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Agency"
        verbose_name_plural = "Agencies"