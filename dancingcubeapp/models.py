from django.db import models
from django.urls import reverse
from .validators import validate_file_extension_for_map, validate_file_extension_for_music, validate_file_extension_for_image
#from django.contrib.sites.models import Site

class Map(models.Model):
    name = models.CharField(max_length=30, default='')
    music = models.FileField(upload_to='media/musics/', validators=[validate_file_extension_for_music])
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
    image = models.ImageField(upload_to='media/musics/', blank=True, null=True, validators=[validate_file_extension_for_image])
    uploader = models.CharField(max_length=200, default='')
    map = models.FileField(upload_to='media/maps/', validators=[validate_file_extension_for_map])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('map-detail', kwargs={'pk': self.pk})
