from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('tutor', 'Tutor'),
        ('student', 'Student'),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)  # Используем EmailField для автоматической валидации
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)  # Тип пользователя
    username = None  # Отключаем стандартное поле username

    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)      # Дата обновления

    USERNAME_FIELD = 'email'  # Используем email для авторизации
    REQUIRED_FIELDS = []      # Убираем обязательные дополнительные поля

    def __str__(self):
        return self.email
