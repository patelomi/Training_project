# Generated by Django 4.0.4 on 2022-06-20 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Attribute', '0008_attribute_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='updated_at',
        ),
    ]