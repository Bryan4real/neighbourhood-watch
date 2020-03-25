from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Neighbourhood(models.Model):
    name=models.CharField(max_lenght=50)
    location=models.CharField(max_lenght=60)
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