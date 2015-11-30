# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chart',
            unique_together=set([('song', 'type')]),
        ),
    ]
