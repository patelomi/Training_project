from django.db import models
from Language.models import *
from Attribute.models import *
from Option.models import *

# Create your models here.
class OptionAttribute(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE)
    option = models.ForeignKey(Option,on_delete=models.CASCADE)