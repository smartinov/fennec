from rest_framework import serializers

from fennec.restapi.notifications.models import Notification


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'source', 'content', 'created_on', 'seen_on')
