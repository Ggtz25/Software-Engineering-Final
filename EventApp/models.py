from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    attendees = models.ManyToManyField(User, related_name='rsvped_events', blank=True)

    def __str__(self):
        return self.title