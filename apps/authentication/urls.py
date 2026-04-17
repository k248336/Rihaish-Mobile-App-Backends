from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignupView, 
    LoginView, 
    SendOTPView, 
    VerifyOTPView, 
    GoogleLoginView, 
    LogoutView, 
    DeleteAccountView,
    ChangePasswordView,
    ResetPasswordView
)

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('google-login', GoogleLoginView.as_view(), name='google_login'),
    path('send-otp', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp', VerifyOTPView.as_view(), name='verify_otp'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('delete-account', DeleteAccountView.as_view(), name='delete_account'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset_password'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
