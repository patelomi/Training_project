from django.db import models
from Language.models import Language
from Attribute.models import *
# Create your models here.

class AttributeTranslation(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    name = models.CharField('Name',max_length=200)