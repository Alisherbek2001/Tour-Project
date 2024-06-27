from django.shortcuts import render
from .serializers import CategorySerializer,TourSerializer,TourServiceSerializer,FeedbackSerializer
from .models import Category,Tour,TourService,Image,Video,Feedback
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from account.models import Agency
from rest_framework.response import Response
from rest_framework import status
import os


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class TourListCreateApiView(ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    def create(self, request, *args, **kwargs):
        data = request.data
        categories = data.getlist('categories', [])
        services = data.getlist('services', [])
        images = request.FILES.getlist('images')
        videos = request.FILES.getlist('videos')

        tour = Tour.objects.create(
            name=data['name'],
            short_description=data['short_description'],
            description=data['description'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            agency=get_object_or_404(Agency, id=data['agency']),
            price=data['price'],
            seats=data['seats'],
            )

        for category_id in categories:
            category = get_object_or_404(Category, id=category_id)
            tour.category.add(category)

        for service in services:
            TourService.objects.create(
                name=service,
                tour=tour
            )

        for image in images:
            Image.objects.create(
                image=image,
                tour=tour
            )

        for video in videos:
            Video.objects.create(
                video=video,
                tour=tour
            )
        serializer = self.get_serializer(tour)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TourRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data

        categories = data.getlist('categories', [])
        services = data.getlist('services', [])
        images = request.FILES.getlist('images')
        videos = request.FILES.getlist('videos')

        instance.name = data.get('name', instance.name)
        instance.short_description = data.get('short_description', instance.short_description)
        instance.description = data.get('description', instance.description)
        instance.start_date = data.get('start_date', instance.start_date)
        instance.end_date = data.get('end_date', instance.end_date)
        instance.agency = get_object_or_404(Agency, id=data.get('agency', instance.agency.id))
        instance.price = data.get('price', instance.price)
        instance.seats = data.get('seats', instance.seats)
        instance.save()

        if categories:
            instance.category.clear()
            for category_id in categories:
                category = get_object_or_404(Category, id=category_id)
                instance.category.add(category)

        if services:
            instance.tourservice_set.all().delete()
            for service in services:
                TourService.objects.create(
                    name=service,
                    tour=instance
                )

        if images:
            for image in instance.image_set.all():
                if os.path.isfile(image.image.path):
                    os.remove(image.image.path)
                image.delete()
            for image in images:
                Image.objects.create(
                    image=image,
                    tour=instance
                )

        if videos:
            for video in instance.video_set.all():
                if os.path.isfile(video.video.path):
                    os.remove(video.video.path)
                video.delete()
            for video in videos:
                Video.objects.create(
                    video=video,
                    tour=instance
                )

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        for image in instance.image_set.all():
            if os.path.isfile(image.image.path):
                os.remove(image.image.path)
            image.delete()
        
        for video in instance.video_set.all():
            if os.path.isfile(video.video.path):
                os.remove(video.video.path)
            video.delete()
        
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
class FeedbackListCreateAPIView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
 
    
class FeedbackRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer