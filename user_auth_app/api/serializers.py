from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegistrationsSerializer(serializers.ModelSerializer):
    """
    Anlegen eines Neuen User Profils
    """

    repeated_password = serializers.CharField(write_only=True)
    color = serializers.CharField(write_only=True, source="profile.color")

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "color"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        pw = self.validated_data["password"]
        repeatet_pw = self.validated_data["repeated_password"]
        profile_data = self.validated_data.pop("profile", {})
        color = profile_data.get("color", "#FFFFFF")
        email = self.validated_data["email"]

        if pw != repeatet_pw:
            raise serializers.ValidationError({"error": "Password don't match!"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email is already in use!"})

        account = User(email=self.validated_data["email"], username=self.validated_data["username"])
        account.set_password(pw)
        account.save()

        profile = account.profile
        profile.color = color
        profile.save()

        return account


class LoginSerializer(serializers.Serializer):
    """
    User Log in Prüfung
    """

    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError({"error": "Falsche E-Mail oder Passwort."}, code="authorization")

        attrs["user"] = user
        return attrs


class GuestCreationSerializer(serializers.Serializer):
    """
    Guest Login
    """

    username = serializers.CharField(read_only=True)
