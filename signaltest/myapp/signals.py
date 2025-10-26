import time
import threading
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import MyModel


@receiver(post_save, sender=MyModel)
def demo_all(sender, instance, **kwargs):
    print("\n=====================")
    print(f"Signal triggered for instance: {instance.name}")
    print(f"Signal thread id: {threading.get_ident()}")
    print(f"Signal start time: {timezone.now()}")

    # Simulate synchronous blocking
    time.sleep(3)
    print(f"Signal end time (after 3s sleep): {timezone.now()}")

    # Print count (shows inside-transaction view)
    print(f"Row count inside signal: {MyModel.objects.count()}")

    # If name matches 'Rollback Test', trigger rollback
    if instance.name == "Rollback Test":
        print("Raising exception to test transaction rollback...")
        raise Exception("Rollback triggered from signal!")

    print("=====================\n")
