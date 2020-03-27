from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Neighbourhood(models.Model):
    name=models.CharField(max_length=50)
    location=models.CharField(max_length=60)
    admin=models.ForeignKey("Profile",on_delete=models.CASCADE,related_name='hood')
    occupants_count=models.IntegerField(null=True,blank=True)
    description=models.TextField()

    def __str__(self):
        return f'{self.name} hood'

    def save_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def find_neighborhood(cls,neighborhood_id):
        return cls.objects.filter(id=neighborhood_id)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name=models.CharField(blank=True,max_length=30)
    email=models.CharField(blank=True,max_length=100)
    status=models.TextField(max_length=100)
    profile_image=models.ImageField(upload_to='images/')
    location=models.CharField(max_length=50,blank=True,null=True)
    neighbourhood = models.ForeignKey('Neighbourhood', on_delete=models.SET_NULL, null=True, related_name='members', blank=True)

    def __str__(self):
        return f'{self.user.username} profile'
