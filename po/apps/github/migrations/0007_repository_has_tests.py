# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0006_auto_20150918_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='has_tests',
            field=models.BooleanField(default=False),
        ),
    ]
