from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse

from .models import Profile, Response
from users.models import User
from .tasks import send_mail_response, send_mail_response_to_author_when_accepted


@receiver(post_save, sender=User)  # Создание профиля нового юзера
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Response)  # Новый отклик
def response_created(sender, instance, created, **kwargs):
    if created:
        send_mail_response.delay(instance.pk)


@receiver(post_save, sender=Response)  # Отклик принят
def response_accepted(sender, instance, created, **kwargs):
    if not created:
        send_mail_response_to_author_when_accepted.delay(instance.pk)
