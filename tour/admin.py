from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    list_per_page = 10
    search_fields = ['name']
admin.site.register(Category,CategoryAdmin)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    
    
class VideosInline(admin.TabularInline):
    model = Video
    extra = 1
 
class ServiceInline(admin.TabularInline):
    model = TourService
    extra = 1   
    
class TourAdmin(admin.ModelAdmin):
    inlines = [ImageInline,VideosInline,ServiceInline]
    list_display = ['name','start_date','end_date','agency','price','seats','average_rating']
    list_per_page = 10
    list_editable = ['price','seats']
    search_fields = ['name','short_description','description']
admin.site.register(Tour, TourAdmin)



class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['tour','user']
    search_fields = ['tour','user','text']
    list_per_page = 10
admin.site.register(Feedback,FeedbackAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ['rating','tour','user']
    list_per_page = 10
admin.site.register(TourRating,RatingAdmin)