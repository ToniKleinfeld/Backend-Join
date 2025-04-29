from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import (
    RegistrationsSerializer,
    CustomAuthTokenSerializer,
)
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

            response = Response(
                {
                    "username": saved_account.username,
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="auth_token",
                value=token.key,
                httponly=True,
                secure=False,
                domain="localhost",
                samesite="Lax",
                max_age=24 * 60 * 60,
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    """
    Login des Benutzer mit Email ,Passwort als return obj mit cookie.token oder Error.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            response = Response(
                {"username": user.username},
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="auth_token",
                value=token.key,
                httponly=True,
                secure=True,
                domain="localhost",
                samesite="Lax",
                max_age=24 * 60 * 60,
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # TODO: secure=True , wenn in Production !!!


class VerifyTokenView(APIView):
    """
    Überprüfung, ob ein Token vorhanden ist.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        token_key = request.COOKIES.get("auth_token")
        if not token_key:
            return Response(
                {"detail": "No token cookie."}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({"detail": "Token is valid."}, status=status.HTTP_200_OK)


class PingCookieView(APIView):
    """
    Gibt 200 OK zurück, wenn das 'auth_token' HttpOnly-Cookie im Request enthalten ist,
    sonst 204 No Content.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        if 'auth_token' in request.COOKIES:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(
            key="auth_token",
            domain="localhost",   
            path="/",             
            samesite="Lax"        
        )

        try:
            request.auth.delete()
        except:
            pass

        return response
