from django.db import models
from django.urls import reverse

class Map(models.Model):
    name = models.CharField(max_length=30, default='')
    music = models.FileField(upload_to='media/musics/', blank=True)
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
    image = models.ImageField(upload_to='media/images/', blank=True)
    uploader = models.CharField(max_length=200, default='')
    map = models.FileField(upload_to='media/maps/', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('map-detail', kwargs={'pk': self.pk})
