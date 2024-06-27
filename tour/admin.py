from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    list_per_page = 10
    search_fields = ['name']
admin.site.register(Category,CategoryAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ['id','image','tour','created_at','updated_at']
admin.site.register(Image,ImageAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ['id','video','tour','created_at','updated_at']
admin.site.register(Video,VideoAdmin)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    
    
class VideosInline(admin.TabularInline):
    model = Video
    extra = 1
    
    
class TourAdmin(admin.ModelAdmin):
    inlines = [ImageInline,VideosInline]
    list_display = ['name','start_date','end_date','agency','price','seats']
    list_per_page = 10
    list_editable = ['price','seats']
    search_fields = ['name','short_description','description']
admin.site.register(Tour, TourAdmin)


class TourServiceAdmin(admin.ModelAdmin):
    list_display = ['name','tour']
    list_per_page = 10
    search_fields = ['name','description']
admin.site.register(TourService,TourServiceAdmin)


# class MediaTourAdmin(admin.ModelAdmin):
#     list_display = ['image','video','tour']
#     list_per_page = 10
# admin.site.register(MediaTour,MediaTourAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['tour','user']
    search_fields = ['tour','user','text']
    list_per_page = 10
admin.site.register(Feedback,FeedbackAdmin)