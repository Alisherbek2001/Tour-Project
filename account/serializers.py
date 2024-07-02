from rest_framework import serializers
from .models import Agency
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['id','name','description','user','image','rating']
        

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'password','confirm_password']
        extra_kwargs = {'password': {'write_only': True}}


    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Password do not match')
        return data
            
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user
