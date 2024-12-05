from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your models here.
class notifyform(models.Model):
    images=models.ImageField(upload_to="imagesfolder")
    date=models.DateTimeField()

class notification(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    notification=models.TextField(max_length=100)
    is_seen=models.BooleanField(default=False)
    
    def save(self,*args,**kwargs):
        channel_layer=get_channel_layer()
        Notification_objs=notification.objects.all(is_seen=False).count()
        data={'count':Notification_objs,'current_notification':self.notification}
        
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group',{
            'type': 'send_notification',
            'value':json.dumps(data)
            }
        )
        super(notification,self).save(*args,**kwargs)