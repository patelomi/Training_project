from django.contrib import admin
from Attribute.models import *
from AttributeTraslation.models import *
from django.http import HttpResponseRedirect
# Register your models here.


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['code', 'inputtype', 'isrequest']

    def changeform_view(self, request, obj, form_url="", extra_context=None):
        lang_data = (
            Language.objects.filter(status="enabled")
        )

        attribute_data = (
            Attribute.objects.all().values()
        )

        if request.method == 'POST': 
            code = request.POST['code']
            inputtype = request.POST['inputtype']
            isrequest = request.POST['isrequest']
            if isrequest == "on":
                isrequest = True
            else:
                isrequest = False
            
            for i in lang_data:
                language = request.POST.get(i.locale+'language')
                language_id = Language.objects.get(locale=language)
                name = request.POST.get(i.locale+'name')

                attributetranslation = AttributeTranslation(language = language_id, name = name)
                attributetranslation.save()

            attribute = Attribute(code = code,inputtype = inputtype,isrequest = isrequest)
            attribute.save()

            from django.contrib import messages
            messages.success(request, ('Add Successfully'))

            return HttpResponseRedirect("/admin/Attribute/attribute/")

       
        extra_context = extra_context or {"lang_data": lang_data,"attribute_data":attribute_data,"obj":obj}
        return super().changeform_view(request, obj, form_url, extra_context=extra_context)


admin.site.register(Attribute, AttributeAdmin)