from allauth.account.forms import SignupForm
from string import hexdigits
import random

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, k=6))
        user.code = code
        user.code_created_at = now()
        user.save()
        subject = 'Подтверждение регистрации на QuestBoard!'
        text = (f"Здравствуйте!\n\nСпасибо за регистрацию. Для подтверждения вашего email введите следующий "
                f"код на сайте: {code}\n\nКод действителен в течение 10 минут.\n\nС уважением, "
                f"команда QueastBoard.")
        html_content = render_to_string('account/email/confirm_code.html', {
            'code': code,
        })
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return user
