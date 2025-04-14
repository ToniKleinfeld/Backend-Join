from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import UserSerializer

class UserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    