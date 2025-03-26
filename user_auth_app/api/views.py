from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# from user_auth_app.models import UserProfile
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import  RegistrationsSerializer ,CustomAuthTokenSerializer
from rest_framework.permissions import IsAuthenticated

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
            data = {
                "token": token.key,
                "username": saved_account.username,
                "email": saved_account.email,
            }
        else:
            data = serializer.errors

        return Response(data)
    
class CustomLoginView(ObtainAuthToken):
    """
    Login des Benutzer mit Email ,Passwort als return obj mit token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomAuthTokenSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email
            }
        else:
            data=serializer.errors

        return Response(data)
