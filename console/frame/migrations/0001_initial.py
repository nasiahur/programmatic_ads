# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-12 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(default=0)),
                ('timestamp', models.IntegerField(default=0)),
            ],
        ),
    ]
