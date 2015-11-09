# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150918_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='source',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
