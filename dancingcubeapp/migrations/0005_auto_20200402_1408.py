# Generated by Django 3.0.3 on 2020-04-02 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dancingcubeapp', '0004_auto_20200227_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/musics/'),
        ),
    ]
