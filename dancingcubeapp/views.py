from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

# Create your views here.

from .models import Map

def index(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

class DashboardView(generic.TemplateView):
    template_name = "dancingcubeapp/dashboard.html"

class MapListView(generic.ListView):
    model = Map

    def get_queryset(self):
        return Map.objects.all()

class MapDetailView(generic.DetailView):
    model = Map 