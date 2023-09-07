from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event."""

    class Meta:
        model = Event
        fields = ["id", "name", "description", "start_date", "end_date"]
