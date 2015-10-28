# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151014_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='has_healthcheck_json',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='deployment',
            name='has_ping_json',
            field=models.BooleanField(default=False),
        ),
    ]
