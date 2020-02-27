from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy, reverse

# Create your views here.

from .models import Map
from .forms import MapForm

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

class MapCreateView(generic.edit.CreateView):
    model = Map
    fields = '__all__'# TODO: add gestion pour que l'uploader soit le user connecté

class MapUpdateView(generic.edit.UpdateView):
    model = Map
    fields = '__all__'

class MapDeleteView(generic.edit.DeleteView):
    model = Map
    success_url = reverse_lazy('dashboard-maps')
