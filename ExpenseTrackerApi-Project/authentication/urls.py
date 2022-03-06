from django.contrib import admin
from django.urls import path
from .views import RegisterView,VerifyEmail,LoginAPIView,RequestPasswordResetEmailAPIView,PasswordTokenCheckAPIView,SetNewPasswordAPIView
from rest_framework_simplejwt.views import (TokenRefreshView,)

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('email-verify/',VerifyEmail.as_view(),name="email-verify"),
    path('login/',LoginAPIView.as_view(),name="login"),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('request-reset-email/',RequestPasswordResetEmailAPIView.as_view(),name="request-reset-email"),
    # Here uidb64, token are params that will be passed to the url..This is the way to mention this
    path('password-reset-check/<uidb64>/<token>/',PasswordTokenCheckAPIView.as_view(),name="password-reset-check"),
    path('password-reset-complete/',SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
]
