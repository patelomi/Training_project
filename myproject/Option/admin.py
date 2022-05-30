from django.contrib import admin
from Option.models import *
from OptionTranslation.models import *
from Language.models import *
# Register your models here.

class OptionAdmin(admin.ModelAdmin):
    def changeform_view(self, request, obj, form_url="", extra_context=None):
            lang_data = (
                Language.objects.filter(status="enabled")
            )

            extra_context = extra_context or {"lang_data": lang_data,"obj":obj}
            return super().changeform_view(request, obj, form_url, extra_context=extra_context)

admin.site.register(Option,OptionAdmin)