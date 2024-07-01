from django.urls import path
from .views import (
    AgencyListCreateAPIView,
    AgencyRetrieveUpdateDestroyAPIView,
    RegisterView,
    LoginView,
    update_password,
    reset_password_with_token
    )

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('agency/',AgencyListCreateAPIView.as_view()),
    path('agency/<int:pk>/',AgencyRetrieveUpdateDestroyAPIView.as_view()),
    path('reset/password/email/', update_password, name='update_password'),
    path('reset/password/email/<uidb64>/<token>/', reset_password_with_token, name='reset_password_with_token'),
]