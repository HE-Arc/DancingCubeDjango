from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy, reverse
import os
from django.conf import settings

from zipfile import ZipFile

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

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

from django.http import Http404
class MapUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Map
    fields = '__all__'
    def get_object(self, queryset=None):
        obj = super(MapUpdateView, self).get_object(queryset)
        print(obj.uploader)
        if obj.uploader != self.request.user.id:
            raise Http404(
                ("You don't own this object")
            )
        else:
            print('y')
        return obj


class MapDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    login_url = 'login'
    model = Map
    success_url = reverse_lazy('dashboard-maps')

def MapDownloadView(request, pk):
    map = Map.objects.get(pk = pk)
    with ZipFile('%s' % map.name, 'w') as zipObj:
        pass
    #    zipObj.write(os.path.join(settings.MEDIA_ROOT, map.music.url))
    #    zipObj.write(map.image)
    #    zipObj.write(map.map)
    print(os.path.join(settings.MEDIA_ROOT, map.music.url))
    #response = HttpResponse(mimetype='application/force-download')
    #response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(map.name)
    #response['X-Sendfile'] = smart_str(map.name)
    #return response
    return redirect('map-detail', pk = pk)
