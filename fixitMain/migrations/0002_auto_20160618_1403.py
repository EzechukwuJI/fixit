# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-18 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fixitMain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategories',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='fixitMain.JobCategories', verbose_name=b'Category'),
        ),
    ]
