# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('statistik', '0021_auto_20151227_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='eloreview',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None, null=True),
        ),
    ]
