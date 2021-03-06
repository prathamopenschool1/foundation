# Generated by Django 2.2.7 on 2020-03-13 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0015_auto_20200311_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilesRelatedToAppsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FileId', models.IntegerField()),
                ('FileType', models.CharField(max_length=100)),
                ('FileUrl', models.URLField(max_length=500)),
                ('DateUpdated', models.CharField(max_length=100)),
                ('NodeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.AppsList')),
            ],
        ),
    ]
