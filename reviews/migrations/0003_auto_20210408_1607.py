# Generated by Django 3.1.7 on 2021-04-08 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0002_auto_20210407_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='downvote',
        ),
        migrations.RemoveField(
            model_name='review',
            name='upvote',
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_for_vote', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='votes',
            field=models.ManyToManyField(related_name='vote', to='reviews.Vote'),
        ),
    ]