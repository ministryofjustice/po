# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='IratStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('incidents_in_last_two_weeks', models.IntegerField(default=0)),
                ('product', models.OneToOneField(to='core.Product')),
            ],
        ),
    ]
