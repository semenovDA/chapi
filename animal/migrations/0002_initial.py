# Generated by Django 4.1.6 on 2023-02-16 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('animal_location', '0001_initial'),
        ('animal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='visitedLocations',
            field=models.ManyToManyField(blank=True, to='animal_location.animallocation'),
        ),
    ]