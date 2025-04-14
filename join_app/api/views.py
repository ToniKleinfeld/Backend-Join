from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, ContactSerializer, UserWithContactsSerializer
from join_app.models import Contact


class UserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserWithContactsSerializer


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
