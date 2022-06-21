# Generated by Django 4.0.4 on 2022-06-20 09:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attribute', '0011_alter_attribute_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]