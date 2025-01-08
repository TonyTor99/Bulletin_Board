from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Profile
from users.models import User


@receiver(post_save, sender=User)  # Создание профиля нового юзера
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
