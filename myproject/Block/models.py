from django.db import models
from tinymce import models as tinymce_models
from Language.models import Language
# Create your models here.

def lan():
    return Language.objects.get(isdefault="Yes")

class Block(models.Model):
    blockid = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=100,unique=True,default=None)
    statusChoice = (
        ('Enabled','Enabled'),
        ('Disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='Enabled')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.slug) 

class BlockTranslation(models.Model):
    btid = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE,default=lan)
    block = models.ForeignKey(Block,on_delete=models.CASCADE)
    title = models.CharField(("Title"),max_length=200)
    content = tinymce_models.HTMLField()

    def __str__(self):
        return str(self.title)