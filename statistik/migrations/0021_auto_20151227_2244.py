# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0020_auto_20151227_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='clickagain_hc',
            field=models.FloatField(null=True, default=None),
        ),
        migrations.AlterField(
            model_name='chart',
            name='clickagain_nc',
            field=models.FloatField(null=True, default=None),
        ),
    ]
