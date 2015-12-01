# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0014_auto_20151201_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='clear_rating',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(13.0), django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='exhc_rating',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(13.0), django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='hc_rating',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(13.0), django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='score_rating',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(13.0), django.core.validators.MinValueValidator(1.0)]),
        ),
    ]
