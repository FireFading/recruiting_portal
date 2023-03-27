import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Skill(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        unique=True, default=uuid.uuid4, primary_key=True, editable=True
    )

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    intro = models.CharField(max_length=250, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(
        blank=True, null=True, upload_to="profile_images", default="anonim.png"
    )
    skills = models.ManyToManyField(Skill, blank=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    github = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        unique=True, default=uuid.uuid4, primary_key=True, editable=True
    )

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    recipient = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        ordering = ["is_read", "-created"]

    def __str__(self):
        return self.subject
