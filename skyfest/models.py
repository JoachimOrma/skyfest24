from django.db import models
from django.utils import timezone

# Create your models here.

class Attendee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    attendee_phone = models.CharField(max_length=15)
    parent_phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=9)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.parent_phone} {self.created_at}"

    class Meta: 
        ordering = ['first_name', 'last_name']

