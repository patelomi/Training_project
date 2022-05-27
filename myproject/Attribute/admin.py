from django.contrib import admin
from Attribute.models import *
# Register your models here.

class AttributeAdmin(admin.ModelAdmin):
    list_display = ['code','inputtype','isrequest']

admin.site.register(Attribute,AttributeAdmin)