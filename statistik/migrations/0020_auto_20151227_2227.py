# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0019_auto_20151210_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='clickagain_hc',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='chart',
            name='clickagain_nc',
            field=models.FloatField(default=0.0),
        ),
    ]
