from rest_framework import viewsets

from fennec.restapi.notifications.serializers import NotificationSerializer
from models import Notification
from rest_framework import filters


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_on')
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.all().order_by('-created_on')
        seen = self.request.QUERY_PARAMS.get('seen', None)
        if seen is not None:
            if str(seen).lower() in ['false']:
                queryset = queryset.filter(seen_on=None)

        return queryset