from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy, reverse
from django.db.models import Q
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
 
def search(request):
    query_term = request.GET.get('q')
    
    qs = filter_maps(query_term)

    context = {
        'results': qs,
        'query_term': query_term
    }

    return render(request, 'dancingcubeapp/search_result.html', context)

def filter_maps(query_term):
    qs = Map.objects.all()

    if query_term != '' and query_term is not None:
        qs = qs.filter(
            Q(name__icontains=query_term) | 
            Q(music__icontains=query_term) | 
            Q(music__icontains=query_term) | 
            Q(uploader__username__icontains=query_term)
        ).distinct()
    
    return qs


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
    fields = ('name', 'music', 'difficulty', 'image', 'map',)

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
    Downloading a map: create a zip on the fly.
    Source: https://chase-seibert.github.io/blog/2010/07/23/django-zip-files-create-dynamic-in-memory-archives-with-pythons-zipfile.html .
    Credit to @Ishydo on Github, thanks.
    """

    map = Map.objects.get(pk = pk)

    zip_files_paths = [
        os.path.join(settings.MEDIA_ROOT, str(map.image)).replace('/', os.sep).replace('\\', os.sep), # dirty ?
        os.path.join(settings.MEDIA_ROOT, str(map.map)).replace('/', os.sep).replace('\\', os.sep), 
        os.path.join(settings.MEDIA_ROOT, str(map.music)).replace('/', os.sep).replace('\\', os.sep), 
    ]
    
    # In memory zip
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
    response["Content-Disposition"] = f"attachment; filename=dancingcube_{map.name}.zip"
    
    in_memory.seek(0)
    response.write(in_memory.read())
    
    return response