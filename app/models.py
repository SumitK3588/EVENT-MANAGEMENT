from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tickets_sold = models.PositiveIntegerField(default=0)  # <-- Added to track sales
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee_name = models.CharField(max_length=100)
    is_checked_in = models.BooleanField(default=False)
    purchase_date = models.DateTimeField(auto_now_add=True)
