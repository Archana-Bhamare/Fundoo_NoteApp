from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
from Note_APp.models import UserProfile


@receiver(signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)