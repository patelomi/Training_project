from django.db import models
from Language.models import Language
from tinymce import models as tinymce_models
# Create your models here.
def lan():
    return Language.objects.get(isdefault="Yes")

class BannerGroup(models.Model):
    bgid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, null=False, unique=True)
    statusChoice = (
        ('Enabled','Enabled'),
        ('Disabled','Disabled'),
    )
    status = models.CharField(max_length=10, choices=statusChoice, default='Disabled')
    sortorder = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.code)

class BannerGroupTranslation(models.Model):
    bgtid = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, default=lan)
    bannergroup = models.ForeignKey(BannerGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name) 

class Banner(models.Model):
    choice = (
        ('Yes','Yes'),
        ('No','No'),
    )
    bid = models.AutoField(primary_key=True)
    sortorder = models.IntegerField()
    isfeatured = models.CharField(max_length=10, choices=choice, default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.bid) 

class BannerTranslation(models.Model):
    btid = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, default=lan)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    title = models.CharField(("Title"),max_length=200)
    content = tinymce_models.HTMLField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.title) 

class BannerImage (models.Model):
    biid = models.AutoField(primary_key=True)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    bannergroup = models.ForeignKey(BannerGroup, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    url = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.url) 