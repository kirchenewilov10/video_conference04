# Generated by Django 2.2.7 on 2020-09-23 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0009_prices_service_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='index',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
