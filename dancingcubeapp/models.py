from django.db import models
from django.urls import reverse
from .validators import validate_file_extension_for_map, validate_file_extension_for_music, validate_file_extension_for_image
#from django.contrib.sites.models import Site
from taggit.managers import TaggableManager

import os

from django.contrib.auth.models import User

class Map(models.Model):
    name = models.CharField(max_length=30, default='')
    music = models.FileField(upload_to=f'media{os.sep}musics{os.sep}', validators=[validate_file_extension_for_music])
    EASY = '1'
    MEDIUM = '2'
    HARD = '3'
    diff_rates = [
        (EASY, 'easy'),
        (MEDIUM, 'medium'),
        (HARD, 'hard'),
    ]
    difficulty = models.CharField(
        max_length=1,
        choices=diff_rates,
        default=EASY
        )
    image = models.ImageField(upload_to=f'media{os.sep}images{os.sep}', blank=True, null=True, validators=[validate_file_extension_for_image])
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    map = models.FileField(upload_to=f'media{os.sep}maps{os.sep}', validators=[validate_file_extension_for_map]) #utile uniquement pour que le champ map soit affiché par le form
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('map-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        ''' Return how much likes this map has. '''
        return self.likes.count()

class MapFile(models.Model):
    file = models.FileField(upload_to=f'media{os.sep}maps{os.sep}', validators=[validate_file_extension_for_map])
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
