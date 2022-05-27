from email.policy import default
from django.db import models

# Create your models here.

class Option(models.Model):
    id = models.AutoField(primary_key=True)
    coustomoption = models.CharField('Custom Option',max_length=200)
    sortorder = models.IntegerField('Sort Order')
    default = models.BooleanField('Default',default=False)
