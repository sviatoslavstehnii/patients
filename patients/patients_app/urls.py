from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('patients_list', views.patients_list, name='patients_list'),
    path('create_patient', views.create_patient, name='create_patient'),
    path('add_visit', views.add_visit, name='add_visit'),
    path('calendar', views.CalendarView.as_view(), name='calendar'),
    path('update_patient/<str:pk>/', views.update_patient, name='update_patient'),
    path('search', views.patients_list, name='search'),
    path('ask_delete/<str:pk>/', views.ask_delete, name='ask_delete')
]
