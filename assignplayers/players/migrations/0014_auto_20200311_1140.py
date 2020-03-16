# Generated by Django 2.2.7 on 2020-03-11 11:40

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0013_auto_20200311_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='appslist',
            name='AppId',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appslist',
            name='DateUpdated',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appslist',
            name='JsonData',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
        migrations.AddField(
            model_name='appslist',
            name='NodeId',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appslist',
            name='NodeTitle',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appslist',
            name='NodeType',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='appslist',
            name='ParentId',
            field=models.CharField(default='', max_length=100),
        ),
    ]
