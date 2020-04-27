from django.db import models
from django.urls import reverse
from .validators import validate_file_extension_for_map, validate_file_extension_for_music, validate_file_extension_for_image
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
import os

class Map(models.Model):
    """ Main model of the website. """

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
    map = models.FileField(upload_to=f'media{os.sep}maps{os.sep}', validators=[validate_file_extension_for_map]) # Only for the form input to render
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    tags = TaggableManager() # Init taggit, to tags our maps

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('map-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        """ Return how much likes this map has. """
        return self.likes.count()
    
    def liked_by_user(self, user_id):
        """ Return True if the user with the user_id already liked the map, else False """
        return self.likes.filter(id=user_id).exists()
    
    def name_without_spaces(self):
        """ Return the name attribute but replaced spaces char with underscores (_) """
        return self.name.replace(' ', '_')

class MapFile(models.Model):
    """ Allow to have multiple files in the map """
    file = models.FileField(upload_to=f'media{os.sep}maps{os.sep}', validators=[validate_file_extension_for_map])
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
