from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User

# Сериализатор для User
class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Повтор пароля

    
    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}


    def validate(self, attrs):
        # Проверка совпадения паролей
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "The password don't match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')  # Удаляем повтор пароля
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Хешируем пароль
        user.save()
        return user

# Сериализатор для токенов
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Вызываем стандартную валидацию для получения токенов
        data = super().validate(attrs)
        # Добавляем name в ответ
        data['name'] = self.user.name
        return data
