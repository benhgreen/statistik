# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0027_song_music_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='id',
            field=models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True),
        ),
    ]
