from . import models
from django.dispatch import receiver
from django.db.models import signals

@receiver(signals.post_save, sender=models.Bus)
def create_seats(sender, instance,created, *args, **kwargs):
    if created:
            for num in range(1, (instance.capacity or 0) + 1):
                  models.Seat.objects.create(bus=instance,seat_number=str(num))