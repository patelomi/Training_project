import re
from django.contrib import admin
from django.shortcuts import redirect, render
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
                
            if request.method == 'POST':
                slug = request.POST['slug']
                sortorder = request.POST['sortorder']
                status = request.POST['status'] 

                page = Pages(slug=slug,sortorder=sortorder,status=status)
                page.save()

                pagesdata = Pages.objects.get(slug = slug)


                for i in lang_data: 
                    title = request.POST[i.locale+'title'] 
                    content = request.POST[i.locale+'content']
                    lang = request.POST[i.locale+'language']
                    langdata = Language.objects.get(locale = lang)

                    PageLanguagedata = PageLanguage(title = title, content = content, pages = pagesdata, language = langdata)
                    PageLanguagedata.save()

        else:
            Pages_data = (
                    PageLanguage.objects.raw("select * from pages_pagelanguage where pages_id = '"+obj+"'")
                )

            if request.method == 'POST':
                slug = request.POST['slug']
                sortorder = request.POST['sortorder']
                status = request.POST['status'] 

                Pages.objects.filter(slug=slug).update(sortorder=sortorder,status=status)
                

                pagesdata = Pages.objects.get(slug = slug)


                for i in lang_data: 
                    id = request.POST.get(i.locale+'id')
                    title = request.POST.get(i.locale+'title') 
                    content = request.POST.get(i.locale+'content')
                    lang = request.POST.get(i.locale+'language')
                    langdata = Language.objects.get(locale = lang)

                    PageLanguage.objects.filter(id=id).update(title = title, content = content, pages = pagesdata, language = langdata)
                    


        extra_context = extra_context or {"lang_data": lang_data,"Pages_data":Pages_data,"page_data":page_data,"obj":obj}
        return super().changeform_view(request, obj,form_url,extra_context=extra_context)

class PageLanguageAdmin(admin.ModelAdmin):
    list_display = ['pages','title','content']   


admin.site.register(Pages,PagesAdmin)
admin.site.register(PageLanguage)