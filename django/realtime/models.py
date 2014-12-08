#coding: utf-8
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import json
import urllib
import urllib2


def send_event(event_type, event_data):
    to_send = {
        'event': event_type,
        'data': event_data
    }
    urllib2.urlopen(settings.ASYNC_BACKEND_URL, urllib.urlencode(to_send)) 


class Message(models.Model):

    user = models.ForeignKey(User)
    text = models.TextField(u"text")
    created_at = models.DateTimeField(u"created at", auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return "%s" % (self.text,)

    def as_dict(self):
        data = {
            'id': self.pk,
            'user': self.user.username,
            'text': self.text,
            'url_delete': reverse("realtime_message_delete", kwargs={'pk':self.pk})
        }
        return json.dumps(data)

    def delete(self, *args, **kwargs):
        pk = self.pk
        super(Message, self).delete(*args, **kwargs)
        send_event('message-delete', pk)

    def save(self, *args, **kwargs):
        is_new = False
        if not self.pk:
            is_new = True
        super(Message, self).save(*args, **kwargs)
        send_event('message-create', self.as_dict())
