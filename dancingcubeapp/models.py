from django.db import models
from django.urls import reverse
#from django.contrib.sites.models import Site

def generate_filename(filename): #it adds the image in a folder with the current year
    ext = filename.split('.')[-1]
    year = datetime.datetime.now().year
    return '/' + str(year) + str(int(time())) + '.' + ext

class Map(models.Model):
    name = models.CharField(max_length=30, default='')
    music = models.FileField(upload_to='media/musics/')
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
    image = models.ImageField(upload_to=generate_filename, blank=True, null=True)
    uploader = models.CharField(max_length=200, default='')
    map = models.FileField(upload_to='media/maps/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('map-detail', kwargs={'pk': self.pk})
