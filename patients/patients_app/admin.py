from django.contrib import admin
from .models import Patient, Event

admin.site.register(Patient)
admin.site.register(Event)