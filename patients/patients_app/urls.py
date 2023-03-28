from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('patients_list', views.patients_list, name='patients_list'),
    path('create_patient', views.create_patient, name='create_patient'),
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