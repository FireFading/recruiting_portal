from django.urls import path

from . import views


urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.user_profile, name='profile'),
    path('skill/<str:skill_slag>', views.profiles_by_skills, name='skill'),
]