# Generated by Django 4.0.4 on 2022-06-07 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Language', '0001_initial'),
        ('Attribute', '0004_remove_attributetranslation_attribute_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='attribute',
            fields=[
                ('attributeId', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('inputType', models.CharField(choices=[('boolean', 'Boolean'), ('checkbox', 'Checkbox'), ('multiselect', 'Multi-select'), ('select', 'Select'), ('radio', 'Radio'), ('textbox', 'Textbox'), ('textarea', 'Textarea')], default='text', max_length=50, verbose_name='Input Type')),
                ('isRequired', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='yes', max_length=10, verbose_name='Is Required')),
            ],
        ),
        migrations.CreateModel(
            name='option',
            fields=[
                ('optionId', models.AutoField(primary_key=True, serialize=False)),
                ('customOption', models.CharField(max_length=100, unique=True, verbose_name='Custom Option')),
                ('sortOrder', models.IntegerField(default=1, verbose_name='Sort Order')),
                ('isDefault', models.BooleanField(default=False, verbose_name='Is Default')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Attribute.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='optionTranslation',
            fields=[
                ('optionTranslationId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Language.language')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Attribute.option')),
            ],
        ),
        migrations.CreateModel(
            name='attributeTranslation',
            fields=[
                ('attributeTranslationId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Attribute.attribute')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Language.language')),
            ],
        ),
    ]
