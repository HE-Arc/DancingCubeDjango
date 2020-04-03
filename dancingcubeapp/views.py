from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy, reverse
import os
from django.conf import settings

from zipfile import ZipFile

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

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
            login(response, user)
            return redirect("index")
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form":form})

def index(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)
    #current_user = request.user
    #if(current_user.has_perm('dancingcubeapp.map.update')):
    #else:
    #return redirect("login")
 
class DashboardView(generic.TemplateView):
    template_name = "dancingcubeapp/dashboard.html"

class MapListView(generic.ListView):
    model = Map

    def get_queryset(self):
        return Map.objects.all()

class MapDetailView(generic.DetailView):
    model = Map

class MapCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Map
    fields = ('name', 'map',)

    def form_valid(self, form):
        uploader = self.request.user
        form.instance.uploader = uploader
        return super(MapCreateView, self).form_valid(form)

class MapUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Map
    fields = '__all__'
    def get_object(self, queryset=None):
        obj = super(MapUpdateView, self).get_object(queryset)
        if obj.uploader == self.request.user or self.request.user.has_perm('dancingcubeapp.map.update'):
            return obj
        else:
            raise Http404(("You don't own this object"))


class MapDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    login_url = 'login'
    model = Map
    success_url = reverse_lazy('dashboard-maps')


from io import BytesIO
from zipfile import ZipFile

def MapDownloadView(request, pk):
    """
    Downloading a zip without saving the zip file on disk.
    """
    print("DOWNLOADING A ZIP OF FILES")

    #map = Map.objects.get(pk = pk)

    # Some file paths
    # To adapt in function of your zip necessities
    zip_files_paths = [
        os.path.join(settings.MEDIA_ROOT, "file1.map"),
        os.path.join(settings.MEDIA_ROOT, "file2.txt")
    ]
    
    # In memory zip ;) What you wanted
    in_memory = BytesIO()
    zip = ZipFile(in_memory, "a")

    # Add files to zip
    for file in zip_files_paths:
        zip.write(file, os.path.basename(file))

    # fix for Linux zip files read in Windows
    for file in zip.filelist:
        file.create_system = 0    
        
    zip.close()

    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=agreatmap.zip"
    
    in_memory.seek(0)    
    response.write(in_memory.read())
    
    return response


