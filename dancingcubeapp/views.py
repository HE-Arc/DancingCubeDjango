from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy, reverse
import os
from django.conf import settings

from zipfile import ZipFile

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
    fields = ('name', 'music', 'difficulty', 'image', 'map',)

    def form_valid(self, form):
        uploader = self.request.user
        form.instance.uploader = uploader
        return super(MapCreateView, self).form_valid(form)

class MapUpdateView(generic.edit.UpdateView):
    model = Map
    fields = '__all__'

class MapDeleteView(generic.edit.DeleteView):
    model = Map
    success_url = reverse_lazy('dashboard-maps')

def MapDownloadView(request, pk):
    map = Map.objects.get(pk = pk)
    with ZipFile('%s' % map.name, 'w') as zipObj:
        pass
    #    zipObj.write(os.path.join(settings.MEDIA_ROOT, map.music.url))
    #    zipObj.write(map.image)
    #    zipObj.write(map.map)
    #print(settings.MEDIA_ROOT,map.music.url)
    musical = map.music.url.replace('/', os.sep)
    print(os.path.join(settings.MEDIA_ROOT, musical[1:]))
    #response = HttpResponse(mimetype='application/force-download')
    #response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(map.name)
    #response['X-Sendfile'] = smart_str(map.name)
    #return response
    return redirect('map-detail', pk = pk)
