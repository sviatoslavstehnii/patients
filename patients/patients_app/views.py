from django.shortcuts import render, redirect

from .models import Patient, CustomUser
from .forms import PatientForm, CustomUserRegistrationForm, EmailAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, get_user_model

def index(request):
    return render(request, 'patients_app/login.html')


def loginn(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User = get_user_model()
            print(email, password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user is not None:
                user = authenticate(request, email=email, password=password)
                # If the email and password match a registered user, log them in
                if user is not None:
                    login(request, user)
                    return redirect('/patients_list')
    else:
        form = AuthenticationForm()
    return render(request, 'patients_app/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/patients_list')
    form = CustomUserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'patients_app/register.html', context)

def create_patient(request):
    """View function for creating a patient."""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        print(form.errors)
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