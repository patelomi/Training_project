from django.contrib import admin
from Attribute.models import *
from AttributeTraslation.models import *
# Register your models here.


class AttributeAdmin(admin.ModelAdmin):
    list_display = ['code', 'inputtype', 'isrequest']

    def changeform_view(self, request, obj, form_url="", extra_context=None):
        lang_data = (
            Language.objects.filter(status="enabled")
        )

        extra_context = extra_context or {"lang_data": lang_data}
        return super().changeform_view(request, obj, form_url, extra_context=extra_context)


admin.site.register(Attribute, AttributeAdmin)