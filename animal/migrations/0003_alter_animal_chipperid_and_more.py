# Generated by Django 4.1.6 on 2023-02-22 00:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_alter_location_latitude_alter_location_longitude'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('animal', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='chipperId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='animal',
            name='chippingLocationId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='location.location'),
        ),
    ]
