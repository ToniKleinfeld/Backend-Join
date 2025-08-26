from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random


def random_hex_color():
    """
    Erstellt eine Zufällig Hex Farbe
    """
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    bgcolor = models.CharField(max_length=10, default=random_hex_color())

    def __str__(self):
        return f"{self.name} ({self.email})"


class Task(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")
    assigned_users = models.ManyToManyField(User, related_name="assigned_tasks", blank=True)
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    RUBRIC_CHOICES = [
        ("To do", "To do"),
        ("In progress", "In progress"),
        ("Await feedback", "Await feedback"),
        ("Done", "Done"),
    ]
    rubric = models.CharField(max_length=20, choices=RUBRIC_CHOICES, default="To do")
    CATEGORY_CHOICES = [
        ("Technical Task", "Technical Task"),
        ("User Story", "User Story"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    PRIORITY_CHOICES = [
        ("low", "low"),
        ("medium", "medium"),
        ("urgent", "urgent"),
    ]
    prio = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")

    def __str__(self):
        return self.title


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class GuestProfile(models.Model):
    """
    Guest User model , mit Ablaufzeit
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="guest_profile")
    expires_at = models.DateTimeField()

    @classmethod
    def create_for_user(cls, user, days=1):

        expires = timezone.now() + timedelta(days=days)
        return cls.objects.create(user=user, expires_at=expires)

    def is_expired(self):
        return timezone.now() > self.expires_at


class Profile(models.Model):
    """
    Profile , wird bei erstellung eines Users per signal hinzugefügt , für zuweisung einer user Farbe
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    color = models.CharField(max_length=10, default=random_hex_color())

    def __str__(self):
        return f"{self.user.username}'s Profile"
