# Generated by Django 3.1.7 on 2021-04-08 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20210407_1950'),
        ('IMDB_user', '0002_auto_20210408_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycustomuser',
            name='seen_list',
        ),
        migrations.AddField(
            model_name='mycustomuser',
            name='favorites_list',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='movies.Movie'),
        ),
    ]
