from django.db.models.signals import post_save
from django.dispatch import receiver

from organization.models import User, UserProfile


@receiver(post_save, sender=User)
def user_profile_create(instance, created, **kwargs):
    if created and instance.is_staff:
        UserProfile.objects.create(user=instance)
