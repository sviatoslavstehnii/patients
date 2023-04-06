from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

class Patient(models.Model):
    """Model representing a patient."""
    SEXES = [('m', 'male'), ('f', 'female')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    sex = models.CharField(choices=SEXES, max_length=1)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    doctor = models.CharField(max_length=200)
    date = models.DateField()
    medical_history = models.TextField()

    def __str__(self) -> str:
        return str(self.name)

    class META:
        """Meta class for Patient model."""
        ordering = ['name']

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def clean(self):
        super().clean()
        if self.start_time >= self.end_time:
            raise ValidationError('Start time must be before end time')
        if self.start_time.time() < datetime.time(hour=9, minute=0):
            raise ValidationError('Start time must be after 9:00 AM')
        if self.end_time.time() > datetime.time(hour=19, minute=0):
            raise ValidationError('End time must be before 7:00 PM')
        if self.start_time.date() != self.end_time.date():
            raise ValidationError('Start time and end time must be on the same day')
        overlapping_events = Event.objects.filter(
            models.Q(start_time__range=(self.start_time, self.end_time)) |
            models.Q(end_time__range=(self.start_time, self.end_time))
        ).exclude(id=self.id)
        if overlapping_events.exists():
            raise ValidationError('This event overlaps with an existing event')
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
