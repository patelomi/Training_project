# Generated by Django 4.0.4 on 2022-07-08 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Banner', '0008_alter_bannergroup_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='bannergroup',
            field=models.ManyToManyField(to='Banner.bannergroup'),
        ),
        migrations.AddField(
            model_name='banner',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='bannerimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bannerimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='bannertranslation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bannertranslation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]