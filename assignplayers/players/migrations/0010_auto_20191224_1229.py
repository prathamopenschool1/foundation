# Generated by Django 2.2.7 on 2019-12-24 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0009_appslist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appslist',
            name='DateUpdated',
            field=models.CharField(max_length=100),
        ),
    ]
