# Generated by Django 4.0.4 on 2022-07-08 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Banner', '0009_banner_bannergroup_banner_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='bannergroup',
        ),
    ]
