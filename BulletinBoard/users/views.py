from random import sample
from string import hexdigits

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.timezone import now, timedelta
from django.views.generic import View

from .models import User


class ConfirmUser(View):
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')  # Получаем код из запроса
        if not code:
            return render(request, 'account/invalid_code.html')  # Если кода нет, показываем ошибку

        # Ищем пользователя с указанным кодом
        user = User.objects.filter(code=code).first()

        if user:
            # Проверяем, не истек ли срок действия кода
            if user.code_created_at and now() <= user.code_created_at + timedelta(minutes=10):
                # Активация пользователя
                user.is_active = True
                user.code = None
                user.code_created_at = None
                user.save()
                return redirect('account_login')  # Успешная активация
            else:
                user.code = None
                user.code_created_at = None
                user.save()
                return render(request, 'account/late_code.html', {'user_id': user.id})  # Если код устарел
        else:
            return render(request, 'account/invalid_code.html')  # Если код неверный

    def get(self, request, *args, **kwargs):
        # Просто отображаем страницу с формой подтверждения
        return render(request, 'account/account_inactive.html')


class RequestNewCode(View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            # Генерируем новый код
            code = ''.join(sample(hexdigits, k=6))
            user.code = code
            user.code_created_at = now()  # Обновляем метку времени
            user.is_active = False  # Убедимся, что пользователь остается неактивным
            user.save()

            # Отправляем новый код на почту
            subject = 'Подтверждение регистрации на QuestBoard!'
            text = (f"Здравствуйте!\n\nДля подтверждения вашего email введите следующий код на сайте: {code}\n\n"
                    f"Код действителен в течение 10 минут.")
            html_content = render_to_string('account/email/confirm_code.html', {'code': code})

            msg = EmailMultiAlternatives(
                subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

            # Перенаправляем обратно на страницу для ввода кода
            return redirect('account_inactive')

        return redirect('account_login')
