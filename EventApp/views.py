from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Event
from datetime import date
import calendar
from django.utils import timezone

def home(request):
    events = Event.objects.all()
    today = timezone.localdate()
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now()
    ).order_by('date')[:5]

    map_events = []
    for event in events:
        map_events.append({
            'id': event.id,
            'title': event.title,
            'location': event.location,
            'date': event.date.strftime('%B %d, %Y %I:%M %p'),
            'latitude': event.latitude,
            'longitude': event.longitude,
        })
    return render(request, 'home.html', {
        'events': events,
        'today': today,
        'upcoming_events': upcoming_events,
        'map_events': map_events,  
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.attendees.add(request.user)
    return redirect('event_detail', event_id=event.id)

def events_view(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def calendar_view(request):
    today = timezone.localdate()
    year = today.year
    month = today.month
    events = Event.objects.filter(date__year=year, date__month=month).order_by('date')
    event_map = {}
    for event in events:
        day = event.date.day
        if day not in event_map:
            event_map[day] = []
        event_map[day].append(event)
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)
    calendar_rows = []
    for week in month_days:
        row = []
        for day in week:
            row.append({
                'day': day,
                'is_today': day == today.day,
                'events': event_map.get(day, []) if day != 0 else [],
            })
        calendar_rows.append(row)
    return render(request, 'calendar.html', {
        'today': today,
        'month_name': calendar.month_name[month],
        'year': year,
        'calendar_rows': calendar_rows,
    })

def map_view(request):  
    events = Event.objects.all()

    map_events = []
    for event in events:
        map_events.append({
            'id': event.id,
            'title': event.title,
            'location': event.location,
            'date': event.date.strftime('%B %d, %Y %I:%M %p'),
            'latitude': event.latitude,
            'longitude': event.longitude,
        })
    return render(request, 'map.html', {
         'map_events': map_events,
         'events': events,
      })