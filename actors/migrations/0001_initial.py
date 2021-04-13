# Generated by Django 3.1.7 on 2021-04-13 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imbd_id', models.CharField(max_length=20)),
                ('name', models.BooleanField(default=False)),
                ('popularity', models.IntegerField(default=0)),
                ('bio', models.CharField(max_length=280)),
            ],
        ),
    ]
