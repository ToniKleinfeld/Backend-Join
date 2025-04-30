from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import (
    ContactSerializer,
    UserSerializer,
    UserWithContactsSerializer,
    TaskSerializer,
    SubTaskSerializer,
    TaskWriteSerializer,
)
from join_app.models import Contact, Task, SubTask
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
class UserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        GET /users/me/
        Response current User.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        
        return Task.objects.filter(
            Q(creator=user) |
            Q(assigned_users=user)
        ).distinct()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TaskWriteSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # TODO: Prüfung funktion , einbindung query in tasks filter?


class SubTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubTaskSerializer

    def get_queryset(self):
        task_pk = self.kwargs.get("task_pk")
        return SubTask.objects.filter(task_id=task_pk)

    def perform_create(self, serializer):
        task_pk = self.kwargs.get("task_pk")
        serializer.save(task_id=task_pk)
