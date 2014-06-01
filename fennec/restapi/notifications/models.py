from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="recipient of the notifications")
    #notification source (could be project/other users/push request etc...
    source = models.CharField(blank=False,max_length=64, help_text="source of the notifications")
    content = models.CharField(blank=False,max_length=256,help_text="content text for the notification")
    created_on = models.DateTimeField(auto_now_add=True,help_text="date and time when the notification was created")
    seen_on = models.DateTimeField(help_text="date when the notification was seen",null=True)

