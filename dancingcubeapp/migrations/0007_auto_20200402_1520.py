# Generated by Django 3.0.3 on 2020-04-02 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dancingcubeapp', '0006_auto_20200402_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
