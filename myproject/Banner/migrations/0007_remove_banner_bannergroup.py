# Generated by Django 4.0.4 on 2022-07-08 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Banner', '0006_alter_bannergroup_sortorder_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='bannergroup',
        ),
    ]