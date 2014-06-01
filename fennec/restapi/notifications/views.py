from rest_framework import viewsets

from fennec.restapi.notifications.serializers import NotificationSerializer
from models import Notification


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_on')
    serializer_class = NotificationSerializer
