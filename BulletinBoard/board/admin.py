from django.contrib import admin
from django.apps import apps
from .models import Ad, Category

from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import site

# Получаем все модели приложения
app_models = apps.get_app_config('board').get_models()

# Регистрируем модели, если они ещё не зарегистрированы
for model in app_models:
    if not site.is_registered(model):
        class GenericAdmin(admin.ModelAdmin):
            list_display = [field.name for field in model._meta.fields]


        admin.site.register(model, GenericAdmin)
