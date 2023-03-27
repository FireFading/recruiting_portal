import contextlib

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from users.models import Profile


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )


def update_user(sender, instance, created, **kwargs):
    profile = instance
    if created == False:
        user = profile.user

        user.first_name = profile.name
        user.username = profile.name
        user.email = profile.email
        user.save()


def delete_user(sender, instance, **kwargs):
    with contextlib.suppress(Exception):
        user = instance.user
        user.delete()


post_save.connect(create_profile, sender=User)
post_save.connect(update_user, sender=Profile)
post_delete.connect(delete_user, sender=Profile)
