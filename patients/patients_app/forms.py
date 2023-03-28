from django import forms
from .models import Patient, Event
from django.forms import ModelForm, DateInput
from datetime import datetime, timedelta

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class EventForm(ModelForm):
  class Meta:
    model = Event
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['start_time'].widget.attrs['min'] = datetime.now().strftime('%Y-%m-%dT%H:%M')
    self.fields['end_time'].widget.attrs['min'] = self.fields['start_time'].widget.attrs['min']