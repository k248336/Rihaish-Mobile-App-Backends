from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from utils.responses import success_response, error_response
from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    OTPSerializer, 
    OTPVerifySerializer, 
    GoogleLoginSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer
)
from .models import OTPVerification
import random
from django.conf import settings
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            # In a real app we might also save phone in UserProfile
            return success_response(
                message="User created successfully",
                data={
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    },
                    "tokens": tokens
                },
                status_code=201
            )
        return error_response(message="Invalid data", data=serializer.errors)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
                if user is not None:
                    tokens = get_tokens_for_user(user)
                    return success_response("Login successful", {"tokens": tokens})
            except User.DoesNotExist:
                pass
            return error_response("Invalid credentials", status_code=401)
        return error_response("Invalid data", data=serializer.errors)


class SendOTPView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = str(random.randint(100000, 999999))
            
            OTPVerification.objects.update_or_create(
                email=email,
                defaults={'otp_code': otp_code, 'is_verified': False}
            )

            if settings.OTP_BACKEND == 'console':
                print(f"\n[DEV] OTP for {email} is {otp_code}\n")
            else:
                # Send OTP via email
                from django.core.mail import send_mail
                try:
                    send_mail(
                        subject='Your Rihaish OTP Code',
                        message=f'Your OTP for Rihaish is: {otp_code}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except Exception as e:
                    return error_response(f"Email error: {str(e)}", status_code=500)

            return success_response("OTP sent successfully", {"email": email})
        return error_response("Invalid data", data=serializer.errors)


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            try:
                otp_record = OTPVerification.objects.get(email=email)
                if otp_record.otp_code == otp_code:
                    otp_record.is_verified = True
                    otp_record.save()
                    return success_response("OTP verified successfully")
                return error_response("Invalid OTP code", status_code=400)
            except OTPVerification.DoesNotExist:
                return error_response("No OTP request found for this email", status_code=404)
        return error_response("Invalid data", data=serializer.errors)


class GoogleLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['access_token']
            try:
                idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
                email = idinfo['email']
                # Create or get user
                user, created = User.objects.get_or_create(username=email, defaults={
                    'email': email,
                    'first_name': idinfo.get('given_name', ''),
                    'last_name': idinfo.get('family_name', '')
                })
                # get tokens
                tokens = get_tokens_for_user(user)
                return success_response("Google login successful", {"tokens": tokens, "is_new_user": created})
            except ValueError:
                return error_response("Invalid Google token", status_code=401)
        return error_response("Invalid data", data=serializer.errors)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success_response("Logged out successfully")
        except Exception as e:
            return error_response("Invalid token", status_code=400)


class DeleteAccountView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            user = request.user
            user.delete()
            return success_response("Account deleted successfully")
        except Exception as e:
            return error_response("Failed to delete account", status_code=400)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return error_response("Old password is incorrect", status_code=400)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return success_response("Password changed successfully")
        return error_response("Invalid data", data=serializer.errors)


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            new_password = serializer.validated_data['new_password']
            
            # Verify OTP first
            try:
                otp_record = OTPVerification.objects.get(email=email)
                if not otp_record.is_verified or otp_record.otp_code != otp_code:
                    return error_response("Invalid or unverified OTP", status_code=400)
            except OTPVerification.DoesNotExist:
                return error_response("No OTP request found for this email", status_code=404)
            
            # Find user by email
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                # Optional: Invalidate OTP after use
                otp_record.is_verified = False
                otp_record.save()
                return success_response("Password reset successfully")
            except User.DoesNotExist:
                return error_response("User with this email not found", status_code=404)
        return error_response("Invalid data", data=serializer.errors)
