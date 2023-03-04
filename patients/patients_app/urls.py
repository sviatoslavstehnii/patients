from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('patients_list', views.patients_list, name='patients_list'),
    path('create_patient', views.create_patient, name='create_patient'),
    path('add_visit', views.add_visit, name='add_visit'),
    path('calendar', views.calendar, name='calendar'),
    path('update_patient/<str:pk>/', views.update_patient, name='update_patient'),
]
