from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy, reverse
from django.db.models import Q
import os
from django.conf import settings

from zipfile import ZipFile

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.utils.translation import gettext as _


# Create your views here.

from .models import Map, MapFile
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

def musicians(request):
    context = {}
    return render(request, 'dancingcubeapp/musician.html', context)

def leveldesigners(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def testers(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)


def devs(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def trailer(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def influenceurs(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def others(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def follow(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def share(request):
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

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
            Q(uploader__username__icontains=query_term)
        ).distinct()

    return qs


class MapListView(generic.ListView):
    model = Map

    def get_queryset(self):
        return Map.objects.all()

class MapDetailView(generic.DetailView):
    model = Map

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_liked'] = True if self.object.likes.filter(id=self.request.user.id).exists() else False
        return context

difficulties = {"1": "EASY", "2": "MEDIUM", "3": "HARD"} # hard-coded, not great

#based on:
#https://stackoverflow.com/questions/38257231/how-can-i-upload-multiple-files-to-a-model-field
class MapCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Map
    fields = ('name', 'music', 'difficulty', 'image', 'map', 'tags')

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        if self.request.FILES:
            obj = form.save(commit=False)
            obj.save()
            for f in self.request.FILES.getlist('map'):
                mapFile = MapFile(file = f, map = obj)
                mapFile.save()

        # Below are 3 attempt to add the difficulty (EASY, MEDIUM or HARD) as a taggit tag.
        # First two attempts creates the tags (in the table *taggit-tag*) but unfortunately does not link the tag with the object (map). no M2M relationship in the *taggit_taggeditem* table...

        # Attempt 1
        """ # saving with commit=False, https://stackoverflow.com/a/51174259/11553000 or the official documentation https://django-taggit.readthedocs.io/en/latest/forms.html
        new_map = form.save(commit=False)
        new_map.uploader =  self.request.user
        new_map.save()
        new_map.tags.add(difficulties[form.cleaned_data["difficulty"]])
        new_map.save() # ?
        form.save_m2m()
        """

        # Attempt 2
        """ # https://stackoverflow.com/a/5361504/11553000
        name = form.cleaned_data['name']
        tags = form.cleaned_data['tags']
        new_map = Map(name=name, uploader=self.request.user)
        new_map.save()
        new_map.tags.add(*tags)
        new_map.tags.add(difficulties[form.cleaned_data["difficulty"]])
        """

        # Attempt 3
        """ # adding by force the tag. Does not work at all.
        #form.cleaned_data["tags"].append(difficulties[form.instance.difficulty]) # add difficulty as tag
        """

        return super(MapCreateView, self).form_valid(form)

    def handle_uploaded_file(f):
        with open('some/file/name.txt', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

class MapUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Map
    fields = ('name', 'music', 'difficulty', 'image', 'map', 'tags')

    def get_object(self, queryset=None):
        obj = super(MapUpdateView, self).get_object(queryset)
        if obj.uploader == self.request.user or self.request.user.has_perm('dancingcubeapp.map.update'):
            map_files = MapFile.objects.filter(map = obj).delete()
            obj.save()
            for f in self.request.FILES.getlist('map'):
                mapFile = MapFile(file = f, map = obj)
                mapFile.save()
            return obj
        else:
            # Translators: user updating a map he doesn't own
            raise Http404(_("You don't own this object"))


class MapDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    login_url = 'login'
    model = Map
    success_url = reverse_lazy('maps')


from io import BytesIO
from zipfile import ZipFile
from django.template.loader import render_to_string

def MapDownloadView(request, pk):
    """
    Downloading a map: create a zip on the fly.
    Source: https://chase-seibert.github.io/blog/2010/07/23/django-zip-files-create-dynamic-in-memory-archives-with-pythons-zipfile.html .
    Credit to @Ishydo on Github, thanks.
    """

    map = Map.objects.get(pk = pk)

    zip_files_paths = [
        os.path.join(settings.MEDIA_ROOT, str(map.image)).replace('/', os.sep).replace('\\', os.sep), # dirty ?
        os.path.join(settings.MEDIA_ROOT, str(map.music)).replace('/', os.sep).replace('\\', os.sep),
    ]

    map_files = MapFile.objects.filter(map = map)

    for map_f in map_files:
        zip_files_paths.append(os.path.join(settings.MEDIA_ROOT, str(map_f.file)).replace('/', os.sep).replace('\\', os.sep),)

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
    print(map.name.replace(" ", "_"))
    response["Content-Disposition"] = f"attachment; filename=dancingcube_{map.name.replace(' ', '_')}.zip"

    in_memory.seek(0)
    response.write(in_memory.read())

    return response

def like_map(request):
    """ Whenever a user like a map, add a like to it. If already like by this user, dislike it.
    User has to be authentificated to like/dislike
    """

    map = get_object_or_404(Map, id=request.POST.get('id')) # Get the map
    is_liked = False

    if request.user.is_authenticated:
        if map.likes.filter(id=request.user.id).exists():
            map.likes.remove(request.user) # dislike
            is_liked = False
        else:
            map.likes.add(request.user) # like
            is_liked = True

    context = {
        'map': map,
        'is_liked': is_liked,
        'total_likes': map.total_likes(), # get the number total of likes
    }

    # return a json respoonse if it's ajax
    if request.is_ajax():
        html = render_to_string('dancingcubeapp/partials/like.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, '')

class TagIndexView(generic.ListView):
    ''' List all maps with related tag, taken from url slug. Example: /maps/tags/mytag/ '''
    model = Map

    def get_queryset(self):
        return Map.objects.filter(tags__slug=self.kwargs['name'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['name']
        return context
