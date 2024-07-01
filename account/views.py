from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from.models import Agency,CustomUser
from .serializers import AgencySerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import status 
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class AgencyListCreateAPIView(ListCreateAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    
    
class AgencyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise AuthenticationFailed("Both email and password are required.")

        user = CustomUser.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            raise AuthenticationFailed("Incorrect email or password.")

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return Response({
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
        })
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def update_password(request):
    user = request.user
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_url = request.build_absolute_uri(reverse('reset_password_with_token', kwargs={'uidb64': uid, 'token': token}))
    
    send_mail(
        'Reset Your Password',
        f'Click the link to reset your password: {reset_url}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    return Response({"detail": "Password reset link has been sent to your email."}, status=200)


@api_view(['GET','POST'])
def reset_password_with_token(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')

            if new_password and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return Response({"detail": "Password updated successfully"}, status=200)
            else:
                return Response({"detail": "Passwords do not match"}, status=400)
        return render(request, 'reset_password.html', {'validlink': True, 'uidb64': uidb64, 'token': token})
    else:
        return render(request, 'reset_password.html', {'validlink': False})
    