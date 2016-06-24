# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-02 18:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fixitCustomers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=7)),
                ('name', models.CharField(max_length=75)),
                ('longitude', models.CharField(max_length=20)),
                ('latitude', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('country', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=20)),
                ('latitude', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='JobCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(help_text=b'A descriptive note about he category in view', max_length=300)),
                ('category_title', models.CharField(max_length=150)),
                ('title_slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobUploads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(max_length=10)),
                ('job_id', models.CharField(max_length=11)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True, verbose_name=b'Date uploaded')),
                ('picture', models.ImageField(blank=True, max_length=125, null=True, upload_to=b'job_images')),
                ('document', models.FileField(blank=True, max_length=125, null=True, upload_to=b'job_documents')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_sent', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PostedJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=10, unique=True)),
                ('job_title', models.CharField(max_length=100, verbose_name=b'Job title')),
                ('description', models.CharField(max_length=300, verbose_name=b'Description')),
                ('start_date', models.CharField(max_length=20, verbose_name=b'Expected start date')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=75)),
                ('area', models.CharField(max_length=75)),
                ('zip_code', models.IntegerField()),
                ('zone_id', models.CharField(max_length=10)),
                ('supplier', models.CharField(max_length=20, verbose_name=b'Materials supplied by:')),
                ('status', models.CharField(max_length=15)),
                ('views', models.IntegerField(default=0, verbose_name=b'Views')),
                ('title_slug', models.SlugField(max_length=110)),
                ('time_frame', models.CharField(max_length=75)),
                ('budget', models.CharField(max_length=75)),
                ('current_stage', models.CharField(max_length=75)),
                ('num_response', models.IntegerField(default=0)),
                ('taken_by', models.CharField(default=b'', max_length=125)),
                ('review', models.TextField(blank=True, max_length=300, null=True)),
                ('edited_on', models.DateTimeField(auto_now_add=True)),
                ('job_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitMain.JobCategories', verbose_name=b'Category')),
            ],
        ),
        migrations.CreateModel(
            name='Responses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responder', models.CharField(max_length=12, verbose_name=b'Tradesman')),
                ('response_note', models.CharField(max_length=300, verbose_name=b'Comment from Tradesman')),
                ('quoted_amount', models.CharField(max_length=10)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('supply_estimate', models.CharField(help_text=b'Estimated amount for materials', max_length=15, verbose_name=b'Estimated amount for materials')),
                ('supply_list', models.CharField(help_text=b'optionally list the needed materials', max_length=500, verbose_name=b'List of materials')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitMain.PostedJob', verbose_name=b'Related To')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('state', models.CharField(max_length=75)),
                ('longitude', models.CharField(max_length=20)),
                ('latitude', models.CharField(max_length=20)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitMain.Country', verbose_name=b'Country')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(help_text=b'A descriptive note about the subcategory in view', max_length=300)),
                ('subcategory_title', models.CharField(max_length=150, verbose_name=b'Sub Category')),
                ('title_slug', models.SlugField(max_length=100, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitMain.JobCategories', verbose_name=b'Category')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=7)),
                ('name', models.CharField(max_length=75)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitMain.State', verbose_name=b'State')),
            ],
        ),
        migrations.AddField(
            model_name='postedjob',
            name='job_sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitMain.SubCategories', verbose_name=b'Sub Category'),
        ),
        migrations.AddField(
            model_name='postedjob',
            name='postedby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitCustomers.Customers', verbose_name=b'Requested by'),
        ),
        migrations.AddField(
            model_name='messages',
            name='related_job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitMain.PostedJob'),
        ),
        migrations.AddField(
            model_name='messages',
            name='sent_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'sender'),
        ),
        migrations.AddField(
            model_name='area',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitMain.State', verbose_name=b'State'),
        ),
        migrations.AddField(
            model_name='area',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitMain.Zone', verbose_name=b'Zone'),
        ),
    ]