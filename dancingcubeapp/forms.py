from django.forms import ModelForm
from django import forms
from django.forms import ClearableFileInput
from .models import Map, MapFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MapForm(ModelForm):
    class Meta:
        model = Map
        fields = '__all__'

class MapFileForm(ModelForm):
    class Meta:
        model = MapFile
        fields = ['file']
        widget = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
