from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# from user_auth_app.models import UserProfile
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import (
    RegistrationsSerializer,
    CustomAuthTokenSerializer,
    TokenVerifySerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class RegestrationView(APIView):
    """
    Regestration des Benutzer mit Name, Email ,Passwort und Passwortkontrolle.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationsSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)

            return Response(
                {
                    "token": token.key,
                    "username": saved_account.username,
                    "email": saved_account.email,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    """
    Login des Benutzer mit Email ,Passwort als return obj mit token oder Error.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {"token": token.key, "username": user.username, "email": user.email},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyTokenView(APIView):
    """
    Überprüfung, ob ein Token vorhanden ist.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenVerifySerializer(data=request.data)
        if serializer.is_valid():
            token_key = serializer.validated_data["token"]
            try:
                token = Token.objects.get(key=token_key)
            except Token.DoesNotExist:
                return Response(
                    {"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED
                )
            return Response({"detail": "Token is valid."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
