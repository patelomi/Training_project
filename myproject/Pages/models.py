from django.db import models
from django.db.models import Model
from tinymce import models as tinymce_models
from django.db import transaction
from Language.models import Language
from django.urls import reverse

# Create your models here.

def lan():
    return Language.objects.get(isdefault="Yes")

class Pages(models.Model):
    slug = models.SlugField(primary_key=True,unique=True)

    statuschoice = (
        ('Enabled','Enabled'),
        ('Disabled','Disabled'),
    )
    status = models.CharField(("Status"),max_length=10,choices=statuschoice,default='Enabled')
    sortorder = models.IntegerField(("Sort Order"),default=0)

    def __str__(self):
        return str(self.slug)
        
    def get_absolute_url(self):
        return reverse("pagedetails", kwargs={"slug": self.slug})    

class PageLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE,default=lan)
    pages = models.ForeignKey(Pages,on_delete=models.CASCADE)
    title = models.CharField(("Title"),max_length=200)
    content = tinymce_models.HTMLField(("Content"))

    def __str__(self):
        return str(self.title)