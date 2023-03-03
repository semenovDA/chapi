# Generated by Django 4.1.6 on 2023-02-16 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalLocation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dateTimeOfVisitLocationPoint', models.DateTimeField(auto_now_add=True)),
                ('locationPointId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.location')),
            ],
        ),
    ]
