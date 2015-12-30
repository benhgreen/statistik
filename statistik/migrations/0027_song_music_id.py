# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0026_auto_20151230_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='music_id',
            field=models.IntegerField(null=True, blank=True, unique=True),
        ),
    ]
