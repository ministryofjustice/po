# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0003_auto_20150917_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='description',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
    ]
