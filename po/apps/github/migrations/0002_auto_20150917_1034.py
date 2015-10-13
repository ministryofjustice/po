# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='repository',
            options={'verbose_name_plural': 'repositories'},
        ),
        migrations.AddField(
            model_name='languageusage',
            name='language',
            field=models.CharField(default=None, max_length=30),
            preserve_default=False,
        ),
    ]
