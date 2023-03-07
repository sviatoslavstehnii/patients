from django.shortcuts import render, redirect

from .models import Patient
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