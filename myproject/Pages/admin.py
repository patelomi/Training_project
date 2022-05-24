from django.contrib import admin
from Pages.models import *
from Language.models import *

# Register your models here.

class PageLanguageInline(admin.StackedInline):
    model = PageLanguage
    extra = 1
    # max_num = Language.objects.count()
    list_display = ['language']

class PagesAdmin(admin.ModelAdmin):
    list_display = ['slug','status']
    inlines = [PageLanguageInline]

class PageLanguageAdmin(admin.ModelAdmin):
    list_display = ['pages','title','content']   


admin.site.register(Pages,PagesAdmin)