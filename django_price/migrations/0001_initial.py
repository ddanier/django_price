# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LinearTax',
            fields=[
                ('tax_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_price.Tax')),
                ('percent', models.DecimalField(max_digits=6, decimal_places=3)),
            ],
            options={
                'abstract': False,
            },
            bases=('django_price.tax',),
        ),
        migrations.CreateModel(
            name='MultiTax',
            fields=[
                ('tax_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_price.Tax')),
            ],
            options={
                'abstract': False,
            },
            bases=('django_price.tax',),
        ),
        migrations.AddField(
            model_name='tax',
            name='_poly_ct',
            field=models.ForeignKey(related_name='+', editable=False, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='multitax',
            name='taxes',
            field=models.ManyToManyField(related_name='+', to='django_price.Tax'),
        ),
    ]