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
 
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginView):
    template_name = 'patients_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('patients_list')

class RegisterPage(FormView):
    template_name = 'patients_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('patients_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('patients_list')
        return super(RegisterPage, self).get(*args, **kwargs)



def index(request):
    """View function for home page of site."""
    return render(request, 'patients_app/index.html')


def create_patient(request):
    """View function for creating a patient."""
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PatientForm(request.POST)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.user = request.user
                patient.save()
                return redirect('/patients_list')
        else:
            form = PatientForm()
        context = {
            'form': form
        }
        return render(request, 'patients_app/create_patient.html', context)
    else:
        return redirect('/login')


def patients_list(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')
        if query:
            patients = Patient.objects.filter(name__icontains=query)
        else:
            patients = Patient.objects.all()
        patients = patients.filter(user=request.user)
        return render(request, 'patients_app/patients_list.html', {'patients': patients})
    else:
        return redirect('/login')

def update_patient(request, pk):
    if request.user.is_authenticated:
        patient = Patient.objects.get(id=pk)
        form = PatientForm(instance=patient)

        if request.method == 'POST':
            form = PatientForm(request.POST, instance=patient)
            if form.is_valid():
                form.save()
                return redirect('/patients_list')

        context = {'form': form}
        return render(request, 'patients_app/update_patient.html', context)
    else:
        return redirect('/login')

def update_event(request, pk):
    if request.user.is_authenticated:
        event = Event.objects.get(id=pk)
        form = EventForm(instance=event)

        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('/calendar')

        context = {'form': form}
        return render(request, 'patients_app/update_event.html', context)
    else:
        return redirect('/login')


def ask_delete(request, pk):
    if request.user.is_authenticated:
        patient = Patient.objects.get(id=pk)

        if request.method == "POST":
            patient.delete()
            return redirect('/patients_list')
        return render(request, 'patients_app/delete.html', {'patient': patient})
    else:
        return redirect('/login')

def delete_event(request, pk):
    if request.user.is_authenticated:
        event = Event.objects.get(id=pk)

        if request.method == "POST":
            event.delete()
            return redirect('/calendar')
        return render(request, 'patients_app/delete_event.html', {'event': event})
    else:
        return redirect('/login')

# def calendar(request):
#     return render(request, 'patients_app/calendar.html')

class CalendarView(LoginRequiredMixin ,generic.ListView):
    model = Event
    template_name = 'patients_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True, request=self.request)
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

def event(request, event_id=None, day_id=None):
    context = {'events': None}
    if day_id:
        events = Event.objects.filter(start_time__day=day_id)
        events = events.filter(user=request.user)
        context['events'] = events
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    if request.method == 'POST':
        form = EventForm(request.POST, instance=instance)
        if form.is_valid():
            events = Event.objects.all()
            events = events.filter(start_time__day=form.cleaned_data['start_time'].day)
            for event in events:
                if event.start_time <= form.cleaned_data['start_time'] <= event.end_time \
                        or event.start_time <= form.cleaned_data['end_time'] <= event.end_time \
                        or (form.cleaned_data['start_time'] <= event.start_time and form.cleaned_data['end_time'] >= event.end_time):
                    return redirect('/event/new')
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return HttpResponseRedirect(reverse('calendar'))
    else:
        form = EventForm(instance=instance)

    context['form'] = form
    return render(request, 'patients_app/event.html', context)