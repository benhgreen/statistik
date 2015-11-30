# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('statistik', '0007_auto_20151114_0154'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('dj_name', models.CharField(max_length=6)),
                ('best_techniques', django.contrib.postgres.fields.ArrayField(size=3, base_field=models.IntegerField(choices=[(0, 'Scratching'), (1, 'Jacks'), (2, 'Speed Changes'), (3, 'Charge Notes'), (4, 'Scales'), (5, 'Chord Scales'), (6, 'Denim')]))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
