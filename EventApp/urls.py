from django.urls import path
from . import views
from .views import signup

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', signup, name='signup'),
    path('events/', views.events_view, name='events'),
    path('event/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('map/', views.map_view, name='map'),
]