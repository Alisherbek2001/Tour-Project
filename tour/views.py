from django.shortcuts import render
from .serializers import CategorySerializer,TourSerializer,TourServiceSerializer,FeedbackSerializer
from .models import Category,Tour,TourService,Image,Video,Feedback
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from account.models import Agency
from rest_framework.response import Response
from rest_framework import status


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
        data = request.data 
        pk = self.kwargs.get('pk')
        try:
            categories = data.getlist('categories', [])
            services = data.getlist('services', [])
            images = request.FILES.getlist('images')
            videos = request.FILES.getlist('videos')
            tour = Tour.objects.get(pk=pk)
            serializer = TourSerializer(tour,data=request.data, partial=(request.method=="PATCH"))
            if serializer.is_valid():
                serializer.save()
                
                for image in images:
                    image.image.delete(save=False)
                    image.delete()
                    
                for image in images:
                    Image.objects.create(
                        image=image,
                        tour=tour
                    )
                for video in videos:
                    video.video.delete(save=False)
                    video.delete()
                    
                for video in videos:
                    Video.objects.create(
                        video=video,
                        tour=tour
                    )    
                    
        except Tour.DoesNotExist:
            return Response('Tour not found',status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        
        
class FeedbackListCreateAPIView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
 
    
class FeedbackRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer