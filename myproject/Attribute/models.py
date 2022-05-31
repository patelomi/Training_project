import select
from django.db import models
from Language.models import Language
# Create your models here.


class Attribute(models.Model):

    selectinput = (
        ('Textbox', 'Textbox'),
        ('Radio', 'Radio'),
        ('Checkbox', 'Checkbox'),
        ('Boolean', 'Boolean'),
        ('Textarea', 'Textarea'),
        ('Multi-select', 'Multi-select'),
        ('Select', 'Select')
    )
    id = models.AutoField(primary_key=True)
    code = models.SlugField('Code', max_length=200)
    inputtype = models.CharField(
        'Input Type', choices=selectinput, max_length=200)
    isrequest = models.BooleanField('Is Request', default=False)

    def __str__(self):
        return str(self.code)

class AttributeTranslation(models.Model):
    id = models.AutoField(primary_key=True)
    attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    name = models.CharField('Name',max_length=200)

class Option(models.Model):
    id = models.AutoField(primary_key=True)
    attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE)
    coustomoption = models.CharField('Custom Option',max_length=200)
    sortorder = models.IntegerField('Sort Order')
    default = models.BooleanField('Default',default=False)

class OptionTranslation(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    option = models.ForeignKey(Option,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)