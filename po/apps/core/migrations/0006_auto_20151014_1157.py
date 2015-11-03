# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150918_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='service',
            field=models.ForeignKey(related_name='products', to='core.Service', null=True),
        ),
    ]
