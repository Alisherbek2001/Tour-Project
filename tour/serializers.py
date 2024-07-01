from rest_framework import serializers
from .models import *
from account.serializers import Agency


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TourServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourService
        fields = '__all__'
  
        
class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video']
    

class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourService
        fields = ['name']
        
        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class TourCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']   

class TourAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['name']  
             
class TourSerializer(serializers.ModelSerializer):
    category = TourCategorySerializer(many=True)
    services = ServiceListSerializer(source='tourservice_set', many=True, read_only=True)
    images = ImageListSerializer(source='image_set', many=True, read_only=True)
    videos = VideoListSerializer(source='video_set', many=True, read_only=True)
    agency = TourAgencySerializer(many=False)
    class Meta:
        model = Tour
        fields = ['id','name','category','agency','services','images','videos','short_description','description','start_date','end_date','price','seats','average_rating']
    