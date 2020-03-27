from rest_framework import serializers
from .models import Neighbourhood, Profile, Business, Post, NeighbourhoodAdmin, SystemAdmin, Contact
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class NeighbourhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighbourhood
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class HoodAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeighbourhoodAdmin
        fields = '__all__'


class SystemAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAdmin
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user