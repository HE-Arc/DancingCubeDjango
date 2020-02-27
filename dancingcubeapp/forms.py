from django.forms import ModelForm
from django import forms
from .models import Map

class MapForm(ModelForm):
    class Meta:
        model = Map
        fields = '__all__'
