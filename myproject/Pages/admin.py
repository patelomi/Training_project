from django.contrib import admin
from Pages.models import *
from Language.models import *
import json
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder

from Pages.views import page_details

# Register your models here.

class PageLanguageInline(admin.StackedInline):
    model = PageLanguage
    extra = 1
    # max_num = Language.objects.count()
    list_display = ['language']

class PagesAdmin(admin.ModelAdmin):
    list_display = ['slug','status']
    # inlines = [PageLanguageInline]

    def changeform_view(self, request, obj, form_url="", extra_context=None):
        lang_data = (
                Language.objects.filter(status = "enabled")
            )
        page_data = (
            Pages.objects.all().values()
        )
        if obj == None:
            Pages_data = (
                PageLanguage.objects.raw("select * from pages_pagelanguage")
            )
        else:
            Pages_data = (
                    PageLanguage.objects.raw("select * from pages_pagelanguage where pages_id = '"+obj+"'")
                )
        extra_context = extra_context or {"lang_data": lang_data,"Pages_data":Pages_data,"page_data":page_data,"obj":obj}
        return super().changeform_view(request, obj,form_url,extra_context=extra_context)

class PageLanguageAdmin(admin.ModelAdmin):
    list_display = ['pages','title','content']   


admin.site.register(Pages,PagesAdmin)
admin.site.register(PageLanguage)