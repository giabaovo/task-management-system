from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    # Serializer for account model 
    class Meta:
        model = Account
        fields = ("email", "password",)
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Handle for create a new user
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = Account(email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        return user
    
    def validate(self, attrs):
        # Handle for validate password field
        errors = []
        email = attrs.get("email")
        email_prefix = email.split("@")[0]
        password = attrs.get("password")

        special_characters = ["$", "#", "@", "!", "*"]

        if len(password) < 8:
            errors.append("Password must at least 8 characters")

        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least 1 upper character")

        if not any(c.islower() for c in password):
            errors.append("Password must contain at least 1 lower character")

        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least 1 digit character")
        
        if not any(c in special_characters for c in password):
            errors.append("Password must contain at least 1 special character")
        
        if email_prefix in password:
            errors.append("Password should not same as email name")

        if errors:
            raise serializers.ValidationError({
                "password": errors
            })

        return attrs

class AccountVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"}
    )

    def validate(self, attrs):
        # Handle for validate password field
        errors = []
        email = attrs.get("email")
        email_prefix = email.split("@")[0]
        password = attrs.get("password")

        special_characters = ["$", "#", "@", "!", "*"]

        if len(password) < 8:
            errors.append("Password must at least 8 characters")

        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least 1 upper character")

        if not any(c.islower() for c in password):
            errors.append("Password must contain at least 1 lower character")

        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least 1 digit character")
        
        if not any(c in special_characters for c in password):
            errors.append("Password must contain at least 1 special character")
        
        if email_prefix in password:
            errors.append("Password should not same as email name")

        if errors:
            raise serializers.ValidationError({
                "password": errors
            })

        return attrs