from django.contrib.auth.models import User
from rest_framework import serializers
from join_app.models import Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "email", "phone"]


class UserWithContactsSerializer(UserSerializer, serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "contacts"]
