from django.db import models
from Language.models import Language
# Create your models here.

class Attribute(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
