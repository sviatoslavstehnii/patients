from django.db import models
from django.urls import reverse

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

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'