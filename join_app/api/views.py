from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import ContactSerializer, UserWithContactsSerializer , TaskSerializer, TaskWriteSerializer
from join_app.models import Contact , Task


class UserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserWithContactsSerializer


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskWriteSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # TODO: Prüfung funktion , einbindung