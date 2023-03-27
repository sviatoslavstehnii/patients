from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('patients_list', views.patients_list, name='patients_list'),
    path('create_patient', views.create_patient, name='create_patient'),
    path('add_visit', views.add_visit, name='add_visit'),
    path('update_patient/<str:pk>/', views.update_patient, name='update_patient'),
    path('update_event/<str:pk>/', views.update_event, name='update_event'),
    path('search', views.patients_list, name='search'),
    path('ask_delete/<str:pk>/', views.ask_delete, name='ask_delete'),
    path('delete_event/<str:pk>/', views.delete_event, name='delete_event'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/events/<int:day_id>', views.event, name='calendar'),
    path('event/edit/<int:event_id>/', views.event, name='event_edit'),
    path('event/new/', views.event, name='event_new'),
]