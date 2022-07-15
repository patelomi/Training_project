from email.mime import image
from typing import List
from django.contrib import admin
from Banner.models import *
from Language.models import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from querystring_parser import parser
# Register your models here.

class BannerGroupAdmin(admin.ModelAdmin):
    list_display = ['code','status','sortorder','created_at','updated_at']

    def changeform_view(self, request, obj, form_url="", extra_context=None):
        lang_data = Language.objects.filter(status="enabled")
        extra_context = extra_context or {}
        extra_context['lang_data'] = lang_data
        if obj == None:
            if request.method == 'POST':
                code = request.POST['code']
                status = request.POST['status']
                sortorder = request.POST['sortorder']

                banner_save = BannerGroup(code = code, status = status, sortorder = sortorder)
                banner_save.save()

                for i in lang_data:
                    name = request.POST[i.locale+'name']
                    lang = request.POST[i.locale+'language']
                    langdata = Language.objects.get(locale=lang)

                    bannergroup = BannerGroup.objects.get(code = code)
                    banner_translation = BannerGroupTranslation(name=name, bannergroup=bannergroup, language=langdata)
                    banner_translation.save()

                messages.success(request, ('Add Successfully'))
                return HttpResponseRedirect("/admin/Banner/bannergroup/")
        
        else:
            banner_groupdata = BannerGroup.objects.filter(bgid = obj)
            bannergroupdata = BannerGroup.objects.raw("select * from banner_bannergroup where bgid = '"+obj+"'")
            extra_context['banner_groupdata'] = banner_groupdata
            extra_context['bannergroupdata'] = bannergroupdata
            bannergrouptran_data = BannerGroupTranslation.objects.raw("select * from banner_bannergrouptranslation where bannergroup_id='"+obj+"'")
            extra_context['bannergrouptran_data'] = bannergrouptran_data

            if request.method == 'POST':
                code = request.POST['code']
                status = request.POST['status']
                sortorder = request.POST['sortorder']

                BannerGroup.objects.filter(code = code).update(code = code, status = status, sortorder = sortorder)

                for i in lang_data:
                    id = request.POST.get(i.locale+'bgtid')
                    name = request.POST.get(i.locale+'name')
                    lang = request.POST.get(i.locale+'language')
                    langdata = Language.objects.get(locale=lang)
                    
                    bannergroup = BannerGroup.objects.get(code = code)
                    BannerGroupTranslation.objects.filter(bgtid=id).update(
                        name=name, bannergroup=bannergroup, language=langdata)
                
                messages.success(request, ('Update Successfully'))
                return HttpResponseRedirect("/admin/Banner/bannergroup/")

        return super().changeform_view(request, obj, form_url, extra_context=extra_context)


class BannerAdmin(admin.ModelAdmin):
    def changeform_view(self, request, obj, form_url="", extra_context=None):
        lang_data = Language.objects.filter(status="enabled")
        bannergroupdata = BannerGroup.objects.all()
        extra_context = extra_context or {}
        extra_context['lang_data'] = lang_data
        extra_context['bannergroupdata'] = bannergroupdata
        # print(bannergroupdata)

        if obj == None:
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                sortorder = request.POST['sortorder']
                isfeatured = request.POST.get('isfeatured')
                if isfeatured == 'on':
                    isfeatured = "Yes"
                else:
                    isfeatured = "No"

                banner_save = Banner(sortorder=sortorder, isfeatured=isfeatured)
                banner_save.save()
                for i in lang_data:
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    lang = request.POST[i.locale+'language']
                    langdata = Language.objects.get(locale=lang)

                    banner = Banner.objects.latest('bid')
                    bannerid = Banner.objects.get(bid = banner.bid)
                    banner_translation = BannerTranslation(title=title, content=content, banner=bannerid, language=langdata)
                    banner_translation.save()

                for i in post_dict['option']:
                    bannergroup = post_dict['option'][i]['bannergroup']
                    bannerimg = request.FILES['image['+str(i)+']']
                    url = post_dict['option'][i]['url']
                    bannergrpId = BannerGroup.objects.get(bgid = bannergroup)
                    # print(bannergrpId)

                    banner = Banner.objects.latest('bid')
                    bannerid = Banner.objects.get(bid = banner.bid)
                    bannerImage = BannerImage(image=bannerimg, bannergroup=bannergrpId, url=url, banner=bannerid)
                    bannerImage.save()

                messages.success(request, ('Add Successfully'))
                return HttpResponseRedirect("/admin/Banner/banner/")
    
        else:
            banner_data = Banner.objects.filter(bid = obj)
            extra_context['banner_data'] = banner_data
            bannertran_data = BannerTranslation.objects.raw("select * from banner_bannertranslation where banner_id='"+obj+"'")
            extra_context['bannertran_data'] = bannertran_data
            banner_image = BannerImage.objects.filter(banner_id = obj)
            for i in banner_image:
                bannergroupid = i.bannergroup
                # print(bannergroupid)
            extra_context['banner_image'] = banner_image
            extra_context['bannergroupid'] = bannergroupid

            if request.method == 'POST':
                # print(request.POST)
                List =[]
                post_dict = parser.parse(request.POST.urlencode())
                if(post_dict.get('bannerimage') is not None):
                    for dlt in post_dict['bannerimage'].values():
                        if type(dlt) == type(List):
                            for i in dlt:
                                BannerImage.objects.filter(biid=i).delete()
                        else:
                            BannerImage.objects.filter(biid=dlt).delete()
                        
                sortorder = request.POST['sortorder']
                isfeatured = request.POST.get('isfeatured')
                if isfeatured == 'on':
                    isfeatured = "Yes"
                else:
                    isfeatured = "No"

                Banner.objects.filter(bid = obj).update(sortorder=sortorder, isfeatured=isfeatured)
                
                for i in lang_data:
                    btid = request.POST.get(i.locale+'btid')
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    lang = request.POST[i.locale+'language']
                    langdata = Language.objects.get(locale=lang)

                    bannerid = Banner.objects.get(bid = obj)
                    BannerTranslation.objects.filter(btid = btid).update(title=title, content=content, banner=bannerid, language=langdata)
                         
                    for i in post_dict['option']:
                        biid = post_dict['option'][i].get('biid',None)
                        bannergroup = post_dict['option'][i]['bannergroup']
                        bannergrpId = BannerGroup.objects.get(bgid = bannergroup)
                        url = post_dict['option'][i].get('url',None)
                        banner = Banner.objects.latest('bid')
                        image = request.FILES.get('image['+str(i)+']',None)
                        
                        
                        if biid == None:
                            if url == None:
                                bannerid = Banner.objects.get(bid = obj)
                                bannerImage = BannerImage(image=image, bannergroup=bannergrpId,banner=bannerid)
                                bannerImage.save()
                                messages.success(request, ('Update Successfully'))
                                return HttpResponseRedirect("/admin/Banner/banner/")
                               
                            else:
                                bannerid = Banner.objects.get(bid = obj)
                                bannerImage = BannerImage(image=image, bannergroup=bannergrpId, url=url, banner=bannerid)
                                bannerImage.save()
                                messages.success(request, ('Update Successfully'))
                                return HttpResponseRedirect("/admin/Banner/banner/")
                               
                        else:
                            if image != None:
                                if image.name.lower().endswith(('.png','.jpg','.jpeg')): #validation for img
                                    picupdate = BannerImage.objects.get(biid = biid)
                                    picupdate.image.delete()
                                    picupdate.image = image
                                    picupdate.save()
                                else:
                                    return HttpResponse("ENTER FILE LIKE .png,.jpg etc!")
                            bannerid = Banner.objects.get(bid = obj)
                            BannerImage.objects.filter(biid = biid).update(bannergroup=bannergrpId, url=url, banner=bannerid)
      
                messages.success(request, ('Update Successfully'))
                return HttpResponseRedirect("/admin/Banner/banner/")

        return super().changeform_view(request, obj, form_url, extra_context=extra_context)
admin.site.register(Banner,BannerAdmin)
admin.site.register(BannerGroup,BannerGroupAdmin)
admin.site.register(BannerTranslation)
admin.site.register(BannerGroupTranslation)
admin.site.register(BannerImage)