# Generated by Django 2.2.7 on 2020-03-11 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0012_appslist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appslist',
            name='AppDesc',
        ),
        migrations.RemoveField(
            model_name='appslist',
            name='AppId',
        ),
        migrations.RemoveField(
            model_name='appslist',
            name='AppName',
        ),
        migrations.RemoveField(
            model_name='appslist',
            name='AppOrder',
        ),
        migrations.RemoveField(
            model_name='appslist',
            name='DateUpdated',
        ),
        migrations.RemoveField(
            model_name='appslist',
            name='ThumbUrl',
        ),
    ]
