# Generated by Django 4.0.4 on 2022-07-07 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Banner', '0004_rename_shortorder_bannergroup_sortorder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bannergroup',
            old_name='bg',
            new_name='bgid',
        ),
    ]
