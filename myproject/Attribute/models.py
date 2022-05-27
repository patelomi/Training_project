import select
from django.db import models
from Language.models import Language
# Create your models here.

class Attribute(models.Model):

    selectinput=(
        ('Textbox','Textbox'),
        ('Radio','Radio'),
        ('Checkbox','Checkbox'),
        ('Boolean','Boolean'),
        ('Textarea','Textarea'),
        ('Multi-select','Multi-select')
    )
    id = models.AutoField(primary_key=True)
    code = models.SlugField('Code',max_length=200)
    inputtype = models.CharField('Input Type',choices=selectinput,max_length=200)
    isrequest = models.BooleanField('Is Request',default=False)
