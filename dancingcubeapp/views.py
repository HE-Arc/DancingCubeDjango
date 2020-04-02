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


import tempfile, zipfile
from wsgiref.util import FileWrapper
def MapDownloadView(request, pk):
    map = Map.objects.get(pk = pk)

    files_path = os.path.join(settings.MEDIA_ROOT, os.sep.join(map.image.url.split('/')[1:]))
    
    '''
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w')
    filename = files_path
    archive.write(filename)
    archive.close()
    wrapper = FileWrapper(open(filename, "rb"))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response
    '''
    
    temp = tempfile.TemporaryFile()
    image_name = 'he-arc-Logo_rouge_transp_dm8u3QG.png'; # Get your file name here.

    with ZipFile(temp, 'w') as export_zip:
        export_zip.write(files_path, image_name)

    wrapper = FileWrapper(open(temp, 'rb'))
    content_type = 'application/zip'
    content_disposition = f'attachment; filename={temp}'

    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = content_disposition
    return response

    """
    files_path = os.path.join(settings.MEDIA_ROOT, os.sep.join(map.image.url.split('/')[1:-1]))
    print(files_path)
    path_to_zip = make_archive(files_path, "zip", files_path)
    response = HttpResponse(FileWrapper(open(path_to_zip,'rb')), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="{filename}.zip"'.format(
        filename = map.name.replace(" ", "_")
    )
    return response
    """