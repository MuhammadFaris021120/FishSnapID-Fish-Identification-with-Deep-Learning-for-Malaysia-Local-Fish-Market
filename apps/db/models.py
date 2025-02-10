from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    fullname = models.CharField(max_length=200)
    email = models.EmailField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

class Fish(models.Model):
    local_name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=200)
    fish_desc = models.TextField()
    safety_desc = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)

class FishCollection(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    captured_location = models.CharField(max_length=200)
    image_path = models.CharField(max_length=200)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    confidence_score = models.FloatField(null=True, blank=True)  
