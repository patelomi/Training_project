from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from querystring_parser import parser
from django.contrib import messages
from django.template.defaulttags import register
from django.contrib import admin
from Attribute.models import *
from Attribute.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from Language.models import Language
# Register your models here.
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class Error(Exception):
    pass

class FetchError(Error):
    pass

class AttributeAdmin(admin.ModelAdmin):
    list_display = ['code', 'inputType', 'isRequired','created_at','updated_at']

    def changeform_view(self, request, obj, form_url, extra_context=None):
        extra_context = extra_context or {}
        lang_data = Language.objects.filter(status="enabled")
        extra_context["language"] = lang_data
        if obj == None:
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                code = post_dict['code']
                input = post_dict['inputtype']
                required = post_dict['required']

                try:
                    attr = attribute(
                        code=code, inputType=input, isRequired=required)
                    attr.save()
                except IntegrityError:
                    messages.error(
                        request, "CODE ALREDY EXIST")
                    return HttpResponseRedirect('/admin/Attribute/attribute/add/')
                
                try:
                    attrId = attribute.objects.get(code=code)
                except ObjectDoesNotExist:
                    return HttpResponse("Exception:Attribute can not fatch!")

                for i in lang_data:

                    name = request.POST[i.locale+'name']
                    lang = request.POST[i.locale+'language']
                    langId = Language.objects.get(locale=lang)

                    try:
                        attrTrans = attributeTranslation(
                            name=name, language=langId, attribute=attrId)
                        attrTrans.save()
                    except ValueError or IntegrityError:
                        messages.error(
                            request, "Exception:Attribute Traslation can not be add!")
                        return HttpResponseRedirect('/admin/Attribute/attribute/add/')

                if input in ('radio', 'checkbox', 'select', 'multiselect'):
                    for i in post_dict['option']:
                        customOption = post_dict['option'][i]['customoption']
                        order = post_dict['option'][i]['order']
                        default = post_dict['option'][i].get('default', None)
                        if default == 'on':
                            defaultval = True
                        else:
                            defaultval = False

                        try:
                            opt = option(
                                customOption=customOption, sortOrder=order, isDefault=defaultval, attribute=attrId)
                            opt.save()
                        except IntegrityError:
                            return HttpResponse("Exception:Option can not be added!")

                        try:
                            optId = option.objects.get(
                                customOption=customOption)
                        except ObjectDoesNotExist:
                            return HttpResponse("Exception:Optin id can not be same!")

                        for lang in lang_data:

                            optName = post_dict['option' +
                                                lang.locale][i]['opname']
                            optLang = post_dict['option' +
                                                lang.locale][i]['oplanguage']
                            optLangId = Language.objects.get(locale=optLang)

                            try:
                                optTrans = optionTranslation(
                                    name=optName, language=optLangId, option=optId)
                                optTrans.save()
                            except IntegrityError:
                                return HttpResponse("Exception:Option Translation can not be add!")

                messages.success(request, code+" Add Successfully!")
                return HttpResponseRedirect('/admin/Attribute/attribute/')

        else:
            attributeDetails = attribute.objects.filter(attributeId=obj)

            extra_context['attributeDetails'] = attributeDetails

            optionDetails = option.objects.raw(
                "select * from attribute_option as o where o.attribute_id ='"+obj+"'")
            extra_context['optionDetails'] = optionDetails
            attributeNames = {}
            attributeTranslationDetails = attributeTranslation.objects.raw(
                "select * from attribute_attributetranslation as at inner join language_language l on at.language_id = l.locale where at.attribute_id='"+obj+"'")

            for lang in lang_data:
                for i in attributeTranslationDetails:

                    if lang.locale == i.locale:
                        attributeNames["attributeTranslationId"] = i.attributeTranslationId
                        attributeNames[lang.locale] = {
                            "language": i.locale, 'name': i.name, 'attributeTranslationId': i.attributeTranslationId}
            extra_context['attributeNames'] = attributeNames
            optionNames = {}
            optionTranslationDetails = optionTranslation.objects.raw(
                "select * from attribute_optiontranslation as ot inner join language_language l on ot.language_id = l.locale inner join attribute_option as o on o.optionId=ot.option_id where o.attribute_id='"+obj+"'")

            for lang in lang_data:
                optionNames[lang.locale] = {}
                for i in optionTranslationDetails:

                    if i.locale == lang.locale:
                        optionNames[lang.locale][i.customOption] = {
                            "language": i.locale, 'name': i.name, "optionTranslationId": i.optionTranslationId}

            extra_context['optionNames'] = optionNames

            try:
                if extra_context['attributeDetails'] is None or extra_context['optionDetails'] is None or extra_context['attributeNames'] is None or extra_context['optionNames'] is None:
                    raise FetchError
            except FetchError:
                return HttpResponse("Exception:Attribute can not be fetch!")

            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())

                if(post_dict.get('deletedata') is not None):
                    for dlt in post_dict['deletedata']:
                        option.objects.filter(
                            optionId=post_dict['deletedata'][dlt]).delete()

                attrId = post_dict['attributeid']
                code = post_dict['code']
                input = post_dict['inputtype']
                required = post_dict['required']

                attr = attribute.objects.filter(attributeId=attrId).update(
                    code=code, inputType=input, isRequired=required)

                for i in lang_data:
                    name = post_dict[i.locale+'name']
                    lang = post_dict[i.locale+'language']
                    langId = Language.objects.get(locale=lang)

                    attrTransId = request.POST[i.locale +
                                               'attributetranslationid']

                    attrTrans = attributeTranslation.objects.filter(
                        attributeTranslationId=attrTransId).update(name=name, language=langId, attribute=attrId)

                if input in ('radio', 'checkbox', 'select', 'multiselect'):
                    for i in post_dict['option']:
                        optId = post_dict['option'][i].get('optionid', None)
                        customOption = post_dict['option'][i]['customoption']
                        order = post_dict['option'][i]['order']
                        default = post_dict['option'][i].get('default', None)

                        if default == 'on':
                            defaultval = True
                        else:
                            defaultval = False

                        if optId == None:
                            try:
                                attribute_id = attribute.objects.get(
                                    attributeId=attrId)
                                opt = option(customOption=customOption, sortOrder=order,
                                             isDefault=defaultval, attribute=attribute_id)
                                opt.save()
                            except IntegrityError:
                                return HttpResponse("Exception:Option can not be add Custom Option Alredy exists!")
                        else:
                            opt = option.objects.filter(optionId=optId).update(
                                customOption=customOption, sortOrder=order, isDefault=defaultval, attribute=attrId)

                        for lang in lang_data:
                            optName = post_dict['option' +
                                                lang.locale][i]['opname']
                            optLang = post_dict['option' +
                                                lang.locale][i]['oplanguage']
                            optTransId = post_dict['option' +
                                                   lang.locale][i].get('optiontranslationid', None)
                            optLangId = Language.objects.get(locale=optLang)

                            if optTransId == None:
                                try:
                                    optId = option.objects.get(
                                        customOption=customOption)
                                    optTrans = optionTranslation(
                                        name=optName, language=optLangId, option=optId)
                                    optTrans.save()
                                except ObjectDoesNotExist or IntegrityError:
                                    return HttpResponse("Exception:Option Translation can not be add!")
                            else:
                                optTrans = optionTranslation.objects.filter(optionTranslationId=optTransId).update(
                                    name=optName, language=optLangId, option=optId)

                else:
                    option.objects.filter(attribute=attrId).delete()
                messages.success(request, code+" Update Successfully")
                return HttpResponseRedirect('/admin/Attribute/attribute/')

        return super(AttributeAdmin, self).changeform_view(request, obj, form_url, extra_context)

admin.site.register(attribute, AttributeAdmin)