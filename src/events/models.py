from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    """Model representing an Event."""

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_events"
    )


class EventRegistration(models.Model):
    """Model representing a User's registration for an Event."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="registered_events"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registered_users"
    )
