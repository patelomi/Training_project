# Generated by Django 4.0.4 on 2022-07-04 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0004_alter_customer_confirmpassword_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
