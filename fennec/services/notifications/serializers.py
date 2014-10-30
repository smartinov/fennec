from rest_framework import serializers

from fennec.services.notifications.models import Notification


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'source', 'content', 'created_on','created_by', 'seen_on')
