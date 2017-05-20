# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0035_auto_20170506_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dancer_name',
            field=models.CharField(null=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dj_name',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='chart',
            name='difficulty',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)]),
        ),
    ]
