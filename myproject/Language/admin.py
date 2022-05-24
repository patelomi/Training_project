from django.contrib import admin
from Language.models import *
from django.utils.html import format_html

# Register your models here.
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['title','locale','icons','isdefault','status']

    def icons(self,obj):
        return format_html(f'<img src ="/media/{obj.icon}" style="height:30; width:30px;">')


admin.site.register(Language,LanguageAdmin)