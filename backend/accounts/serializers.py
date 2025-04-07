from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer to register a new user.
    Validates that the password and its confirmation match,
    and enforces password validation rules.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text="User's password (must meet the required criteria)."
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Password confirmation to ensure both passwords match."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        """
        Ensure both passwords match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """
        Create and return a new user with an encrypted password.
        """
        validated_data.pop('password2')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
