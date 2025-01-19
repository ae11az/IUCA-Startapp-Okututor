from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User

# Сериализатор для регистрации пользователя
class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Повтор пароля
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)  # Добавляем поле для типа пользователя
    
    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "password2", "user_type"]
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
            email=validated_data['email'],
            user_type=validated_data['user_type']  # Устанавливаем тип пользователя
        )
        user.set_password(validated_data['password'])  # Хешируем пароль
        user.save()
        return user

# Сериализатор для получения информации о пользователе
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'user_type', 'created_at', 'updated_at']
        read_only_fields = ['email', 'created_at', 'updated_at']

# Сериализатор для токенов
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Вызываем стандартную валидацию для получения токенов
        data = super().validate(attrs)
        # Добавляем name в ответ
        data['name'] = self.user.name
        return data
