from django.db import models
from django.contrib.auth.models import User
import uuid


class Skill(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True, editable=True)
    
    def __str__(self):
        return self.name
        

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    intro = models.CharField(max_length=250, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='profile_images', default='anonim.png')
    skills = models.ManyToManyField(Skill, blank=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    github = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True, editable=True)
    
    def __str__(self):
        return self.user.username
