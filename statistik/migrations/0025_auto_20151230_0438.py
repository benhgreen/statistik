# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0024_auto_20151230_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='alt_artist',
            field=models.CharField(blank=True, null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='song',
            name='alt_title',
            field=models.CharField(blank=True, null=True, max_length=64),
        ),
    ]
