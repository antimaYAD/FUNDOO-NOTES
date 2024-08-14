from django.urls import path
from .views import RegistrationUser, LoginUser

urlpatterns = [
    path('register/', RegistrationUser.as_view(), name='register_user'),
    path('login/', LoginUser.as_view(), name='login_user'),
]
