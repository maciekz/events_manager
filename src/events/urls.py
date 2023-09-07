from rest_framework.routers import DefaultRouter

from events.views import EventViewSet

events_router = DefaultRouter()
events_router.register(r"events", EventViewSet, basename="event")
urlpatterns = events_router.urls
