# Generated by Django 2.2.7 on 2020-08-20 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstantMessageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=255)),
                ('recipient', models.CharField(blank=True, max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='timestamp')),
                ('body', models.TextField(verbose_name='body')),
                ('status', models.IntegerField(blank=True, default=0)),
                ('type', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'instantmessage',
                'verbose_name_plural': 'instantmessages',
                'ordering': ('-timestamp',),
            },
        ),
    ]
