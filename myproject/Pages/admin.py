from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from Pages.models import *
from Language.models import *
# from Pages.views import page_details

# Register your models here.

class PageLanguageInline(admin.StackedInline):
    model = PageLanguage
    extra = 1
    list_display = ['language']


class PagesAdmin(admin.ModelAdmin):
    list_display = ['slug', 'status','created_at','updated_at']

    # Quars for sending data
    def changeform_view(self, request, obj, form_url="", extra_context=None):
        lang_data = (
            Language.objects.filter(status="enabled")
        )

        page_data = (
            Pages.objects.all().values()
        )

        # If Form is blank
        if obj == None:
            Pages_data = (
                PageLanguage.objects.raw("select * from pages_pagelanguage")
            )

            if request.method == 'POST':
                slug = request.POST['slug']
                sortorder = request.POST['sortorder']
                status = request.POST['status']

                page = Pages(slug=slug, sortorder=sortorder, status=status)
                page.save()

                pagesdata = Pages.objects.get(slug=slug)

                # update slug data
                for i in lang_data:
                    title = request.POST[i.locale+'title']
                    content = request.POST.get(i.locale+'content')
                    lang = request.POST[i.locale+'language']
                    langdata = Language.objects.get(locale=lang)

                    PageLanguagedata = PageLanguage(
                        title=title, content=content, pages=pagesdata, language=langdata)
                    PageLanguagedata.save()

                from django.contrib import messages
                messages.success(request, ('Add Successfully'))

                return HttpResponseRedirect("/admin/Pages/pages/")

        # if form is field
        else:
            Pages_data = (
                PageLanguage.objects.raw(
                    "select * from pages_pagelanguage where pages_id = '"+obj+"'")
            )

            if request.method == 'POST':
                slug = request.POST['slug']
                sortorder = request.POST['sortorder']
                status = request.POST['status']

                Pages.objects.filter(slug=slug).update(
                    sortorder=sortorder, status=status)

                pagesdata = Pages.objects.get(slug=slug)

                # update data
                for i in lang_data:
                    id = request.POST.get(i.locale+'id')
                    title = request.POST.get(i.locale+'title')
                    content = request.POST.get(i.locale+'content')
                    lang = request.POST.get(i.locale+'language')
                    langdata = Language.objects.get(locale=lang)

                    PageLanguage.objects.filter(id=id).update(
                        title=title, content=content, pages=pagesdata, language=langdata)

            # inner join qry
            listof_data = (
                PageLanguage.objects.raw(
                    "select * from pages_pagelanguage as pl inner join pages_pages as p on pl.pages_id=p.slug inner join language_language as lan on pl.language_id = lan.locale where pl.pages_id = '"+obj+"'")
            )

            list_data = {}
            for l in lang_data:
                for i in listof_data:
                    if l.locale == i.locale:
                        list_data[l.locale] = i
            # print(list_data)

            # getting joing qry data
            for i in listof_data:
                list_data = {i.locale, i.title, i.slug, i.sortorder,
                             i.language, i.pages, i.title, i.content}
                print(list_data)

        extra_context = extra_context or {
            "lang_data": lang_data, "Pages_data": Pages_data, "page_data": page_data, "obj": obj}
        return super().changeform_view(request, obj, form_url, extra_context=extra_context)


class PageLanguageAdmin(admin.ModelAdmin):
    list_display = ['pages', 'title', 'content']


admin.site.register(Pages, PagesAdmin)
