from django.db import models
from users.models import User

from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):  # Профиль пользователя
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username


class Category(models.Model):  # Категории
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Ad(models.Model):  # Объявления
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=64)
    content = RichTextUploadingField()
    category = models.ManyToManyField(Category, through='AdCategory', related_name='category')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Response(models.Model):  # Отклики
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='responses')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)


class AdCategory(models.Model):  # Промежуточная модель многие ко многим
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
