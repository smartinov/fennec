from django.db import models
# Create your models here.


class TableSymbol(models.Model):
    id = models.AutoField(primary_key=True)
    position_x = models.FloatField()
    position_y = models.FloatField()
    width = models.FloatField(default=100)
    height = models.FloatField(default=100)
    color = models.CharField(max_length=6)
    is_collapsed = models.BooleanField()

    class Meta:
        ordering = ('id',)
