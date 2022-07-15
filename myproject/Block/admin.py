from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from Block.models import *
from Language.models import *
from django.contrib import messages
from django.template.defaulttags import register
from querystring_parser import parser
# Register your models here.

...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

class BlockAdmin(admin.ModelAdmin):
    list_display = ['slug','status','created_at','updated_at']

    def changeform_view(self, request, obj, form_url="", extra_context=None):
        lang_data = Language.objects.filter(status="enabled")
        extra_context = extra_context or {}
        extra_context['lang_data'] = lang_data
        if obj == None:
            if request.method == 'POST':
                print(request)
                slug = request.POST['slug']
                status = request.POST['status']

                block_save = Block(slug=slug, status=status)
                block_save.save()

                for i in lang_data:
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    lang = request.POST[i.locale+'language']
                    langdata = Language.objects.get(locale=lang)
                    print(title,content,lang)

                    block = Block.objects.get(slug=slug)
                    Block_t = BlockTranslation(title=title, content=content, block=block, language=langdata)
                    Block_t.save()

                messages.success(request, ('Add Successfully'))
                return HttpResponseRedirect("/admin/Block/block/")
        
        else:
            block_data = Block.objects.filter(blockid = obj)
            beforblockdata = Block.objects.raw("select * from block_block where blockid='"+obj+"'")
            for before in beforblockdata:
                beforeslug = before.slug
            bt_data = BlockTranslation.objects.raw("select * from block_blocktranslation where block_id='"+obj+"'")
            extra_context['block_data'] = block_data
            extra_context['bt_data'] =bt_data

            if request.method == 'POST':
                slug = request.POST['slug']
                status = request.POST['status']
                
                block_update = Block.objects.filter(slug=slug).update(status=status)

                for i in lang_data:
                    id = request.POST.get(i.locale+'btid')
                    title = request.POST.get(i.locale+'title')
                    content = request.POST.get(i.locale+'content')
                    lang = request.POST.get(i.locale+'language')
                    langdata = Language.objects.get(locale=lang)
                    
                    block = Block.objects.get(slug=slug)
                    BlockTranslation.objects.filter(btid=id).update(
                        title=title, content=content, block=block, language=langdata)
                
        return super().changeform_view(request, obj, form_url, extra_context=extra_context)

admin.site.register(Block,BlockAdmin)
admin.site.register(BlockTranslation)