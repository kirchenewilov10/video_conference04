# Generated by Django 2.2.7 on 2020-09-02 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_contactus'),
    ]

    operations = [
        migrations.CreateModel(
            name='devicetypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='oss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]