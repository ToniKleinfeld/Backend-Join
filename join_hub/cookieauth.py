import datetime
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token

class CookieTokenAuthentication(BaseAuthentication):
    """
    Liest 'auth_token' Cookie aus und prüft, ob es Gültig ist.
    """
    def authenticate(self, request):
        token_key = request.COOKIES.get('auth_token')
        if not token_key:
            return None

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token in cookie')

        return (token.user, token)


class ExpiringCookieTokenAuthentication(BaseAuthentication):
    """
    Liest 'auth_token' Cookie aus und prüft, ob es älter als ein Tag ist.
    """
    def authenticate(self, request):
        token_key = request.COOKIES.get('auth_token')
        if not token_key:
            return None

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if timezone.now() > token.created + datetime.timedelta(days=1):
            
            token.delete()
            raise exceptions.AuthenticationFailed('Token expired.')

        return (token.user, token)