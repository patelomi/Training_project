# Generated by Django 4.0.4 on 2022-06-07 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Attribute', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='option',
            old_name='id',
            new_name='optionId',
        ),
    ]