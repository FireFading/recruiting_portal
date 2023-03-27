from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Message, Profile, Skill


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "email",
            "city",
            "intro",
            "bio",
            "image",
            "skills",
            "telegram",
            "github",
        ]
        labels = {
            "name": "Username",
            "email": "Email",
            "city": "City",
            "intro": "Introduction",
            "bio": "bio",
            "image": "Image",
            "skills": "Skills",
            "telegram": "Telegram",
            "github": "GitHub",
        }
        widgets = {"skills": forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
            field.widget.attrs.update({"class": "form-control"})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "slug", "description"]
        labels = {"name": "Skill Name", "slug": "slug", "description": "Description"}

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name": "Name",
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
