from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from django.views import generic
from .utils import Calendar
from .forms import PatientForm, EventForm
import calendar as clndr
from django.urls import reverse
from .models import *
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    """View function for home page of site."""
    return render(request, 'patients_app/index.html')


def create_patient(request):
    """View function for creating a patient."""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/patients_list')

    form = PatientForm()
    context = {
        'form': form
    }
    return render(request, 'patients_app/create_patient.html', context)



def patients_list(request):
    query = request.GET.get('q')
    if query:
        patients = Patient.objects.filter(name__icontains=query)
    else:
        patients = Patient.objects.all()
    return render(request, 'patients_app/patients_list.html', {'patients': patients})


def update_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    form = PatientForm(instance=patient)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('/patients_list')

    context = {'form': form}
    return render(request, 'patients_app/update_patient.html', context)


def ask_delete(request, pk):
    patient = Patient.objects.get(id=pk)

    if request.method == "POST":
        patient.delete()
        return redirect('/patients_list')
    return render(request, 'patients_app/delete.html', {'patient': patient})


def add_visit(request):
    return render(request, 'patients_app/add_visit.html')

def calendar(request):
    return render(request, 'patients_app/calendar.html')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'patients_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = clndr.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'patients_app/event.html', {'form': form})