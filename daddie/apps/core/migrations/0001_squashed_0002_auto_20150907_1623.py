# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('environment', models.CharField(max_length=30)),
                ('build', models.ForeignKey(related_name='deployments', to='core.Build')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('contact_name', models.CharField(max_length=30)),
                ('contact_email', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='service',
            field=models.ForeignKey(related_name='products', to='core.Service'),
        ),
        migrations.AddField(
            model_name='deployment',
            name='product',
            field=models.ForeignKey(related_name='deployments', to='core.Product'),
        ),
        migrations.AddField(
            model_name='build',
            name='dependencies',
            field=models.ManyToManyField(to=b'core.Package', through='core.Dependency'),
        ),
        migrations.AddField(
            model_name='build',
            name='product',
            field=models.ForeignKey(related_name='builds', to='core.Product'),
        ),
        migrations.AddField(
            model_name='build',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 7, 13, 44, 7, 306952, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deployment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 7, 13, 44, 17, 383315, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='build',
            name='name',
            field=models.CharField(unique=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(unique=True, max_length=30),
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='AlertType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('priority', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='alert',
            name='category',
            field=models.ForeignKey(related_name='alerts', to='core.AlertType'),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('major', models.IntegerField(default=0)),
                ('minor', models.IntegerField(default=0)),
                ('patch', models.IntegerField(default=0)),
                ('extra_version', models.CharField(max_length=30)),
                ('source', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='dependency',
            name='build',
            field=models.ForeignKey(default=None, to='core.Build'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dependency',
            name='package',
            field=models.ForeignKey(related_name='dependants', default=None, to='core.Package'),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='dependency',
            options={'verbose_name_plural': 'dependencies'},
        ),
        migrations.AddField(
            model_name='alert',
            name='package',
            field=models.ForeignKey(related_name='alerts', default=None, to='core.Package'),
            preserve_default=False,
        ),
    ]
