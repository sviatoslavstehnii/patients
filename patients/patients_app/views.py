from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from django.utils.safestring import mark_safe
from django.views import generic
from .utils import Calendar
from .models import Patient, Event
from .forms import PatientForm

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

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()