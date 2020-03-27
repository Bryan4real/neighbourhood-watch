from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
@receiver(post_save, sender=User)
def create_hood_admin(sender, instance, created, **kwargs):
    if created:
        NeighbourhoodAdmin.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_hood_admin(sender, instance, **kwargs):
    instance.neighbourhoodadmin.save()
@receiver(post_save, sender=User)
def create_system_admin(sender, instance, created, **kwargs):
    if created:
        SystemAdmin.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_system_admin(sender, instance, **kwargs):
    instance.systemadmin.save()

class Neighbourhood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    occupants_count = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=80, blank=True)
    status = models.TextField(max_length=254, blank=True)
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    location = models.CharField(max_length=50, blank=True, null=True)
    neighbourhood = models.ForeignKey('Neighbourhood', on_delete=models.SET_NULL, null=True, related_name='members', blank=True)

    def __repr__(self):
        return self.user

class Business(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    description = models.TextField()
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=30, blank=True)
    post = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Contact(models.Model):
    service_name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
    def __str__(self):
        return self.service_name

class SystemAdmin(models.Model):
    is_admin = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __bool__(self):
        return self.is_admin

class NeighbourhoodAdmin(models.Model):
    is_hood_admin = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __bool__(self):
        return self.is_hood_admin
