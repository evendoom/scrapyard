from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=60)
