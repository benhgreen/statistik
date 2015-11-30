# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('type', models.SmallIntegerField(choices=[(0, 'SPN'), (1, 'SPH'), (2, 'SPA'), (3, 'DPN'), (4, 'DPH'), (5, 'DPA')])),
                ('difficulty', models.SmallIntegerField()),
                ('note_count', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('music_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(unique=True, max_length=64)),
                ('alt_title', models.CharField(null=True, max_length=64)),
                ('artist', models.CharField(max_length=64)),
                ('alt_artist', models.CharField(null=True, max_length=64)),
                ('genre', models.CharField(max_length=64)),
                ('bpm_min', models.SmallIntegerField()),
                ('bpm_max', models.SmallIntegerField()),
                ('game_version', models.SmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='chart',
            name='song',
            field=models.ForeignKey(to='statistik.Song'),
        ),
    ]
