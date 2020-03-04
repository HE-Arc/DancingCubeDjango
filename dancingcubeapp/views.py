from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate
# Create your views here.

from .models import Map
from .forms import MapForm
from .forms import RegisterForm

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form":form})

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