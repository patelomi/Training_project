from django.contrib import admin
from Attribute.models import *
from django.http import HttpResponseRedirect
# Register your models here.

class AttributeTranslationAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'language', 'name']

class OptionAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'coustomoption', 'sortorder','default']

class AttributeAdmin(admin.ModelAdmin):
    list_display = ['code', 'inputtype', 'isrequest']

    def changeform_view(self, request, obj, form_url="", extra_context=None):
        lang_data = (
            Language.objects.filter(status="enabled")
        )

        attribute_data = (
            Attribute.objects.all().values()
        )

        option_data = (
            Option.objects.all().values()
        )

        if request.method == 'POST': 
            code = request.POST['code']
            inputtype = request.POST['inputtype']
            isrequest = request.POST.get('isrequest')
            coustomoption = request.POST['option']
            sortorder = request.POST['sortorder']
            isdefault = request.POST.get('isdefault')

            if isdefault == "on":
                isdefault = True
            if isrequest == "on":
                isrequest = True
            else:
                isrequest = False
                isdefault = False

            attribute = Attribute(code = code,inputtype = inputtype,isrequest = isrequest)
            attribute.save()

            attribute_id = Attribute.objects.get(code=code)

            option = Option(coustomoption = coustomoption, sortorder = sortorder, default = isdefault ,attribute=attribute_id)
            option.save()

            option_id = Option.objects.get(coustomoption = coustomoption)

            for i in lang_data:
                language = request.POST.get(i.locale+'language')
                language_id = Language.objects.get(locale=language)
                name = request.POST.get(i.locale+'name')
                nameoption = request.POST.get(i.locale+'nameoption')

                attributetranslation = AttributeTranslation(language = language_id, name = name,attribute=attribute_id)
                attributetranslation.save()

                optiontranslation = OptionTranslation(language = language_id, option = option_id, name = nameoption)
                optiontranslation.save()

            from django.contrib import messages
            messages.success(request, ('Add Successfully'))

            return HttpResponseRedirect("/admin/Attribute/attribute/")

       
        extra_context = extra_context or {"lang_data": lang_data,"attribute_data":attribute_data,"obj":obj}
        return super().changeform_view(request, obj, form_url, extra_context=extra_context)


admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(AttributeTranslation, AttributeTranslationAdmin)
admin.site.register(OptionTranslation)