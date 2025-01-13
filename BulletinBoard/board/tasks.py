from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Response, Ad
from users.models import User


@shared_task
def send_mail_response(response_pk):
    response = Response.objects.get(pk=response_pk)
    email = response.ad.author.user.email

    subject = 'На QuestBoard новый отклик!'
    text = (f"Здравствуйте!\n\nНа объявление {response.ad.title} откликнулись!"
            f"Содержание отклика: {response.content}\n Время отклика: {response.created_at}")
    html_content = render_to_string('response/mail_response_author.html', {
        'response': response,
    })
    msg = EmailMultiAlternatives(
        subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=[email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_mail_response_to_author_when_accepted(response_pk):
    response = Response.objects.get(pk=response_pk)
    email = response.author.user.email

    subject = 'Ваш отклик принят!'
    text = f"Здравствуйте!\n\nВы оставляли отклик на {response.ad.title} и его приняли!"

    html_content = render_to_string('response/mail_response_accepted.html', {
        'response': response,
    })
    msg = EmailMultiAlternatives(
        subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=[email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_send():
    last_week = timezone.now() - timezone.timedelta(days=7)
    posts = Ad.objects.filter(created_at__gte=last_week)
    users = User.objects.all()

    for user in users:
        subject = 'Объявления за последнюю неделю'
        text = f"Здравствуйте!\nВот объявления за последнюю неделю:\n" + "\n".join(
            [f"- {post.title}: http://127.0.0.1:8000/ads/{post.id}" for post in posts]
        )
        html_content = render_to_string('mail_weekly_send.html', {
            'posts': posts,
        })
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
