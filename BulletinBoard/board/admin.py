from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import site

# Список приложений, которые нужно обработать
app_names = ['board', 'users']

# Обрабатываем каждое приложение
for app_name in app_names:
    app_models = apps.get_app_config(app_name).get_models()

    # Регистрируем модели, если они ещё не зарегистрированы
    for model in app_models:
        if not site.is_registered(model):
            class GenericAdmin(admin.ModelAdmin):
                list_display = [field.name for field in model._meta.fields]

            admin.site.register(model, GenericAdmin)
