# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    def set_version(apps, schema_editor):
        Song = apps.get_model("statistik", "Song")
        for song in Song.objects.all():
            song.game = song.game_version // 100
            song.save()

    dependencies = [
        ('statistik', '0034_auto_20170506_2225'),
    ]

    operations = [
        migrations.RunPython(set_version),
    ]
