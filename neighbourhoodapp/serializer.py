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