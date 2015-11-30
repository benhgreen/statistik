# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0011_auto_20151130_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='max_reviewable',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(0)]),
        ),
    ]
