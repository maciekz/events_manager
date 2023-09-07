from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny

from events_auth.serializers import RegisterAccountSerializer


class RegisterAccountView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterAccountSerializer
