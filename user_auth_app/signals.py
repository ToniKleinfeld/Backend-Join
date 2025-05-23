from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from join_app.models import Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Fügt einem neuen User Profile model hinzu
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()