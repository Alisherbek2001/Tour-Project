from django.urls import path
from .views import *


urlpatterns = [
    path('category/',CategoryListCreateAPIView.as_view()),
    path('category/<int:pk>/',CategoryRetrieveUpdateDestroyAPIView.as_view()),
    path('',TourListCreateApiView.as_view()),
    path('<int:pk>/',TourRetrieveUpdateDestroyAPIView.as_view()),
    path('feedback/',FeedbackListCreateAPIView.as_view()),
    path('feedback/<int:pk>/',FeedbackRetrieveUpdateDestroyAPIView.as_view()),
]