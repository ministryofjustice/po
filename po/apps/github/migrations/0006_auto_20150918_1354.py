# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0005_auto_20150917_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='name',
            field=models.CharField(unique=True, max_length=100, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='languageusage',
            unique_together=set([('repository', 'language')]),
        ),
    ]
