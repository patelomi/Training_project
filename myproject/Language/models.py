from django.db import models
from django.db.models import Model
from tinymce import models as tinymce_models
from django.db import transaction

# Create your models here.
class Language(models.Model):

    choice = (
        ('Yes','Yes'),
        ('No','No'),
    )

    statuschoice = (
        ('Enabled','Enabled'),
        ('Disabled','Disabled'),
    )
    title = models.CharField(("Title"),max_length=200)
    locale = models.CharField(primary_key=True,max_length=200,unique=True)
    icon = models.ImageField(("Icon"),upload_to="images/")
    isdefault = models.CharField(("Is Default"),max_length=10,choices=choice,default=False)
    status = models.CharField(("Status"),max_length=10,choices=statuschoice,default='Enabled')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.title)
    
    def save(self,*args,**kwargs):
        if self.isdefault == "No":
            return super(Language,self).save(*args,**kwargs)
        with transaction.atomic():
            Language.objects.filter(
                isdefault="Yes").update(isdefault="No")
            return super(Language,self).save(*args,**kwargs)
