# Generated by Django 2.2.7 on 2019-12-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_auto_20191205_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='playersdatastore',
            name='key_id',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
