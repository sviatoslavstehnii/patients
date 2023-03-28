from django.db import models
from django.urls import reverse
import datetime
from django.core.exceptions import ValidationError

class Patient(models.Model):
    """Model representing a patient."""
    SEXES = [('m', 'male'), ('f', 'female')]
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
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def clean(self):
        super().clean()
        if self.start_time > self.end_time:
            raise ValidationError('Start time must be before end time')
        if self.start_time == self.end_time:
            raise ValidationError('Start time must be before end time')
        if self.end_time.time() >= datetime.time(hour=19):
            raise ValidationError('End time must be before 19:00')
        if self.start_time.date() != self.end_time.date():
            raise ValidationError('Start and end time must be on the same day')
        if self.start_time.time() < datetime.time(hour=9):
            raise ValidationError('Start time must be after 09:00')
    

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'