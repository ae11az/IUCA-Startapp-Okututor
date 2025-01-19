from django.urls import path
from api.views import RegisterView, MyTokenObtainPairView, LogoutView, UserDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # Регистрация пользователя
    path("logout/", LogoutView.as_view(), name="logout"),        # Выход из системы
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),  # Авторизация (получение токена)
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),        # Обновление токена
    path("profile/", UserDetailView.as_view(), name="user_detail"),            # Просмотр/обновление профиля
]
