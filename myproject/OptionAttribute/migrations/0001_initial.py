# Generated by Django 4.0.4 on 2022-05-27 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Option', '0001_initial'),
        ('Attribute', '0001_initial'),
        ('Language', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionAttribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Attribute.attribute')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Language.language')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Option.option')),
            ],
        ),
    ]
