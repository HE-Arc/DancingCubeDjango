# Generated by Django 3.0.3 on 2020-04-27 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dancingcubeapp', '0010_mapfile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mapfile',
            old_name='parentMap',
            new_name='map',
        ),
    ]
