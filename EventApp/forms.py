from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'date',
            'latitude',
            'longitude',
        ]

        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }