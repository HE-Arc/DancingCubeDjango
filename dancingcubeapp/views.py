from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.conf import settings

import os
from zipfile import ZipFile
from io import BytesIO
from zipfile import ZipFile

from .models import Map, MapFile
from .forms import MapForm
from .forms import RegisterForm

def register(response):
    """ Register function for signup """
    
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
    """ Home page """
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def musicians(request):
    """ Musician page (url name: musicians) """
    context = {}
    return render(request, 'dancingcubeapp/musician.html', context)

def leveldesigners(request):
    """ Level designers page (url name: leveldesigners) """
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def testers(request):
    """ Testers page (url name: testers) """
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)


def devs(request):
    """ Devs page (url name: devs) """
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def trailer(request):
    """ Trailer page (url name: trailer) """
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def influenceurs(request):
    """ Influenceurs  page (url name: influenceurs) """
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def others(request):
    """ Others page (url name: others) """
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def follow(request):
    """ Follow page (url name: follow) """
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def share(request):
    """ Share page (url name: share) """
    context = {}
    return render(request, 'dancingcubeapp/index.html', context)

def search(request):
    """ When performing a research (Search page) """
    
    query_term = request.GET.get('q') # Getting the query term (Getter arg)
    qs = filter_maps(query_term) # Calling the filter function

    context = {
        'results': qs,
        'query_term': query_term
    }

    return render(request, 'dancingcubeapp/search_result.html', context)

def filter_maps(query_term):
    """ Filtering maps when performing a research base on an arg (query_term).
    Filter based on the name of the map, the name of the music, and the uploader's username.
    """
    
    qs = Map.objects.all() # All maps

    if query_term != '' and query_term is not None:
        qs = qs.filter(
            Q(name__icontains=query_term) |
            Q(music__icontains=query_term) |
            Q(uploader__username__icontains=query_term)
        ).distinct()

    return qs


class MapListView(generic.ListView):
    """ Listing all maps page (url name: maps) """

    model = Map

    def get_queryset(self):
        return Map.objects.all()

class MapDetailView(generic.DetailView):
    """ Specific map page (url name: map-detail) """

    model = Map

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        # Adding to context if the current user already liked this specific map
        context['is_liked'] = self.object.liked_by_user(self.request.user.id)

        return context

class MapCreateView(LoginRequiredMixin, generic.edit.CreateView):
    """ Form page, to create a map by a user. (url name: map-create)
    Multiple files upload source: https://stackoverflow.com/q/38257231
    """

    model = Map
    fields = ('name', 'music', 'difficulty', 'image', 'map', 'tags')

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        if self.request.FILES:
            obj = form.save(commit=False)
            obj.save()
            for f in self.request.FILES.getlist('map'):
                if f.size > 1024*1024*2:
                    return redirect("map-create")
                map_file = MapFile(file = f, map = obj)
                map_file.save()

        # Below are 3 attempt to add the difficulty (EASY, MEDIUM or HARD) as a taggit tag.
        # First two attempts creates the tags (in the table *taggit-tag*) but unfortunately does not link the tag with the object (map). 
        # Unfortunately, there is no M2M relationship in the *taggit_taggeditem* table...
        # Fore more informations and how we tried to handle it: https://github.com/HE-Arc/DancingCubeDjango/issues/8

        # difficulties = {"1": "EASY", "2": "MEDIUM", "3": "HARD"} # hard-coded, not great

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
    """ Whenever someones is trying to edit a map. (url name: map-update).
    This operation is only for the owner of the uploader or an admin. Throw a 404 else.
    """

    model = Map
    fields = ('name', 'music', 'difficulty', 'image', 'map', 'tags')

    def get_object(self, queryset=None):
        print("salut1")
        obj = super(MapUpdateView, self).get_object(queryset)
        if obj.uploader == self.request.user or self.request.user.has_perm('dancingcubeapp.map.update'):
            map_files = MapFile.objects.filter(map = obj)
            if map_files.exists():
                map_files.delete()
                obj.save()
                print("salu2t")
            for f in self.request.FILES.getlist('map'):
                print(f)
                mapFile = MapFile(file = f, map = obj)
                mapFile.save()
            return obj
        else:
            # Translators: user updating a map he doesn't own
            raise Http404(_("You don't own this object"))

class MapDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    """ 'Are you sure you want to delete this map ?' page. (url name: map-delete) """

    login_url = 'login'
    model = Map
    success_url = reverse_lazy('maps')

def MapDownloadView(request, pk):
    """
    Downloading a map: create a zip on the fly.
    Source: https://chase-seibert.github.io/blog/2010/07/23/django-zip-files-create-dynamic-in-memory-archives-with-pythons-zipfile.html .
    Credit to @Ishydo on Github, thanks.
    """

    map = Map.objects.get(pk = pk) # Getting current map

    zip_files_paths = [
        os.path.join(settings.MEDIA_ROOT, str(map.image)).replace('/', os.sep).replace('\\', os.sep), # dirty ?
        os.path.join(settings.MEDIA_ROOT, str(map.music)).replace('/', os.sep).replace('\\', os.sep),
    ]

    # handling multiple files
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
    response["Content-Disposition"] = f"attachment; filename=dancingcube_{map.name_without_spaces()}.zip"

    in_memory.seek(0)
    response.write(in_memory.read())

    return response

def like_map(request):
    """ Whenever a user like a map, add a like to it. If already like by this user, dislike it.
    User has to be authentificated to like/dislike.
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
    """ List all maps with related tag, taken from url slug. Example: /maps/tags/mytag/ """
    model = Map

    def get_queryset(self):
        return Map.objects.filter(tags__slug=self.kwargs['name']) # Filters all maps with the Getter argument (tag name)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['name'] # the Getter argument (tag name) in the context
        return context