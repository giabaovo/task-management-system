from rest_framework.views import APIView, status
from rest_framework.response import Response

from accounts.serializers import AccountSerializer, AccountVerifySerializer, ResetPasswordSerializer
from accounts.email import send_verify_email, send_verify_forgot_password_email, check_expire_email
from accounts.models import Account
from django.contrib.auth.hashers import check_password


class AccountRegister(APIView):
    # Register API for account
    def post(self, request):
        data = request.data
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Send email to verify to login for account
            send_verify_email(serializer.validated_data.get("email"))
            return Response({"status": "success", "message": "User register successfully"}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class AccountVerify(APIView):
    # API send email verfiy to activate account
    def post(self, request):
        serializer = AccountVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            otp = serializer.validated_data.get("otp")

            user = Account.objects.get(email=email)

            if not user:
                return Response({"status": "error", "message": "User with email {} don't exist".format(email)}, status=status.HTTP_400_BAD_REQUEST)
 
            check_expire_email(otp, user.otp, user.otp_created_at)

            if user.is_active:
                return Response({"status": "error", "message": "This account has been active"}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()

            return Response({"status": "success", "message": "Your account has been active"}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class ResendAccountVerifyEmail(APIView):
    # API resend email for activate account
    def post(self, request):
        email = request.data.get("email")

        user = Account.objects.get(email=email)

        if user:
            send_verify_email(user.email)
            return Response({"status": "success", "message": "OTP code has been send to your email"}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "User with email {} don't exist".format(email)}, status=status.HTTP_400_BAD_REQUEST)
    

class ForgotPassword(APIView):
    def post(self, request):
        email = request.data.get("email")

        user = Account.objects.get(email=email)

        if user:
            send_verify_forgot_password_email(user.email)
            return Response({"status": "success", "message": "OTP code has been send to your email"}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "User with email {} don't exist".format(email)}, status=status.HTTP_400_BAD_REQUEST)
    

class ForgotPasswordVerify(APIView):
    # API send email verfiy to activate account
    def post(self, request):
        serializer = AccountVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            otp = serializer.validated_data.get("otp")

            user = Account.objects.get(email=email)

            if not user:
                return Response({"status": "error", "message": "User with email {} don't exist".format(email)}, status=status.HTTP_400_BAD_REQUEST)
 
            check_expire_email(otp, user.otp, user.otp_created_at)

            return Response({"status": "success", "message": ""}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPassword(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data.get("password")
            email = serializer.validated_data.get("email")

            user = Account.objects.get(email=email)

            if user:
                user.set_password(new_password)
                user.save()

                return Response({"status": "success", "message": "Your password has been updated"}, status=status.HTTP_200_OK)
            return Response({"status": "error", "message": "User with email {} don't exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)              
                    