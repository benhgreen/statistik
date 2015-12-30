# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0023_auto_20151229_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='clickagain_hc',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chart',
            name='clickagain_nc',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
