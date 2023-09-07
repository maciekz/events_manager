from datetime import date

from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from events.models import Event, EventRegistration
from events.permissions import IsCreator
from events.serializers import EventSerializer


class EventViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for events."""

    serializer_class = EventSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ("update", "partial_update"):
            permission_classes = (IsAuthenticated, IsCreator)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == "my_list":
            return Event.objects.filter(creator=self.request.user)
        else:
            return Event.objects.all()

    def perform_create(self, serializer):
        # Set Event creator automatically
        serializer.save(creator=self.request.user)

    @action(detail=False, methods=("GET",))
    def my_list(self, request: Request):
        # Return list() but with a different queryset
        return self.list(request)

    @action(detail=True, methods=("POST", "DELETE"))
    def registration(self, request: Request, *args, **kwargs):
        event = self.get_object()
        if request.method == "POST":
            # Create registration
            return self._create_registration(event)
        else:
            # Delete registration
            return self._delete_registration(event)

    def _create_registration(self, event: Event) -> Response:
        today = date.today()
        # Check if event's start date is in the future
        if event.start_date <= today:
            response_data = {"detail": _("Users can register only to future events.")}
            response_status = status.HTTP_403_FORBIDDEN
        # Check if user has already registered to the event
        elif EventRegistration.objects.filter(
            user=self.request.user, event=event
        ).exists():
            response_data = {"detail": _("User is already registered to the event.")}
            response_status = status.HTTP_403_FORBIDDEN
        # Create new registration
        else:
            EventRegistration.objects.create(user=self.request.user, event=event)
            response_data = {"detail": _("User has registered to the event.")}
            response_status = status.HTTP_201_CREATED
        return Response(response_data, status=response_status)

    def _delete_registration(self, event: Event) -> Response:
        today = date.today()
        queryset = EventRegistration.objects.filter(user=self.request.user, event=event)
        # Check if event's start date is in the future
        if event.start_date <= today:
            response_data = {
                "detail": _("Users can unregister only from future events.")
            }
            response_status = status.HTTP_403_FORBIDDEN
        # Check if user is registered to the event
        elif not queryset.exists():
            response_data = {"detail": _("User is not registered to the event.")}
            response_status = status.HTTP_404_NOT_FOUND
        # Remove registration
        else:
            queryset.delete()
            response_data = {"detail": _("User has unregistered from the event.")}
            response_status = status.HTTP_204_NO_CONTENT

        return Response(response_data, status=response_status)
