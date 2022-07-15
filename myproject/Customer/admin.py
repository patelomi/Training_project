from django.contrib import admin
from Customer.models import *
from Customer.forms import *
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import format_html
from querystring_parser import parser
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import random
from datetime import datetime
# Register your models here.

class AddressAdmin(admin.TabularInline):
    model = Address

class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ['name','isdefault','created_at','updated_at']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['firstname','lastname','profile_pic','email','emailvarifaction','phoneno','group','created_at','updated_at']

    def profile_pic(self,obj):
        return format_html(f'<img src ="/media/{obj.profileimg}" style="height:50; width:50px;">')

    #function for add / update
    def changeform_view(self, request, obj, form_url, extra_context=None):
        customergroupdata = CustomerGroup.objects.all().values()
        citydata = City.objects.all()
        statedata = State.objects.all()
        extra_context = extra_context or {}
        extra_context['customergroupdata'] = customergroupdata
        extra_context['citydata'] = citydata
        extra_context['statedata'] = statedata
        if obj == None:
            if request.method == 'POST':       
                post_dict = parser.parse(request.POST.urlencode())
                fname = request.POST['fname']
                lname = request.POST['lname']
                profileimg = request.FILES.get('profileimg')
                email = request.POST['email']
                phoneno = request.POST['phoneno']
                password = request.POST['password']
                getpass = password.split(" ")
                joinpass = "".join(getpass)
                passwordSave = make_password(joinpass)
                group = request.POST['group']
                cgid = CustomerGroup.objects.get(id = group)
                varification = request.POST.get('varification')
                if varification == 'on':
                    varification = "Yes"
                    today = datetime.now()
                    data = Customer(group=cgid, firstname=fname, lastname=lname, profileimg=profileimg, email=email, phoneno=phoneno, password=passwordSave, emailvarificationdate=today, emailvarifaction=varification)
                    data.save()

                    for i in post_dict['option']:
                        customerid = Customer.objects.latest('cid')
                        cid = Customer.objects.get(cid = customerid.cid)
                        street = post_dict['option'][i]['street']
                        houseno = post_dict['option'][i]['houseno']
                        unitno = post_dict['option'][i]['unitno']
                        postalcode = post_dict['option'][i]['postalcode']
                        tag = post_dict['option'][i]['tag']
                        isdefault = post_dict['option'][i].get('isdefault', None)
                        if isdefault == 'on':
                            defaultval = "Yes"
                        else:
                            defaultval = "No"
                        name = post_dict['option'][i]['name']
                        city = post_dict['option'][i]['city']
                        cityid = City.objects.get(cityid = city)
                        state = post_dict['option'][i]['state']
                        sid = State.objects.get(stateid = state)

                        dataaddress = Address(customer=customerid, name=name, streetname=street, houseno=houseno, unitno=unitno, postalcode=postalcode, tag=tag, isdefault=defaultval, city=cityid ,state=sid)
                        dataaddress.save()

                    messages.success(request," Add Successfully!")
                    return HttpResponseRedirect('/admin/Customer/customer/')
                
                else:
                    #email sent
                    varification = "No" 
                    code=random.randint(0000,999999)  #create randome code 
                    today = datetime.now()
                    html_content = render_to_string("email.html",{"code":code,"name":fname})
                    text_content = strip_tags(html_content)
                    emailsend = EmailMultiAlternatives(
                    "Link FOR VERIFICATION",
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [email],
                    )
                    emailsend.attach_alternative(html_content,"text/html")
                    emailsend.send()                
                    data = Customer(group=cgid, firstname=fname, lastname=lname, profileimg=profileimg, email=email, phoneno=phoneno, password=passwordSave, emailvarifaction=varification, code=code, time=today)
                    data.save()
                    
                    for i in post_dict['option']: #list of data
                        customerid = Customer.objects.latest('cid')
                        cid = Customer.objects.get(cid = customerid.cid)
                        street = post_dict['option'][i]['street']
                        houseno = post_dict['option'][i]['houseno']
                        unitno = post_dict['option'][i]['unitno']
                        postalcode = post_dict['option'][i]['postalcode']
                        tag = post_dict['option'][i]['tag']
                        isdefault = post_dict['option'][i].get('isdefault', None)
                        if isdefault == 'on':
                            defaultval = "Yes"
                        else:
                            defaultval = "No"
                        name = post_dict['option'][i]['name']
                        city = post_dict['option'][i]['city']
                        cityid = City.objects.get(cityid = city)
                        state = post_dict['option'][i]['state']
                        sid = State.objects.get(stateid = state)
                        dataaddress = Address(customer=customerid, name=name, streetname=street, houseno=houseno, unitno=unitno, postalcode=postalcode, tag=tag, isdefault=defaultval, city=cityid ,state=sid)
                        dataaddress.save()
                           
                    messages.success(request," Add Successfully!")
                    return HttpResponseRedirect('/admin/Customer/customer/')    
        
        else:
            form = Address()
            customerdata = Customer.objects.filter(cid = obj)
            customergroupdata = CustomerGroup.objects.all().values()
            citydata = City.objects.all()
            statedata = State.objects.all()
            addressdata = Address.objects.raw("select * from customer_address as a inner join customer_customer as c on a.customer_id = c.cid where a.customer_id='"+obj+"'")
            extra_context['citydata'] = citydata
            extra_context['statedata'] = statedata
            extra_context['addressdata'] = addressdata
            extra_context['customerdata'] = customerdata
            extra_context['customergroupdata'] = customergroupdata
            beforeupdate = Customer.objects.raw("select * from customer_customer where cid='"+obj+"'")

            for b in beforeupdate: #for old data
                beforepass = b.password
                beforeemail = b.email
            
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                cid = request.POST['cid']
                fname = request.POST['fname']
                lname = request.POST['lname']
                profileimg = request.FILES.get('profileimg', None)
                email = request.POST['email']
                phoneno = request.POST['phoneno']
                password = request.POST['password1']
                group = request.POST['group']
                cgid = CustomerGroup.objects.get(id = group)
                if profileimg != None:
                    if profileimg.name.lower().endswith(('.png','.jpg','.jpeg')): #validation for img
                        picupdate = Customer.objects.get(cid = obj)
                        picupdate.profileimg.delete()
                        picupdate.profileimg = profileimg
                        picupdate.save()
                    else:
                        return HttpResponse("ENTER FILE LIKE .png,.jpg etc!")
                varification = request.POST.get('varification')

                if varification == 'on' or varification == None and email == beforeemail:
                    varification = "Yes"
                    today = datetime.now()
                    if password != '':
                        getpass = password.split(" ")
                        joinpass = "".join(getpass)
                        passwordUpdate = make_password(joinpass)
                        Customer.objects.filter(cid = obj).update(group=cgid, firstname=fname, lastname=lname, email=email, phoneno=phoneno, password=passwordUpdate, emailvarificationdate=today, emailvarifaction=varification)

                    else:
                        Customer.objects.filter(cid = obj).update(group=cgid, firstname=fname, lastname=lname, email=email, phoneno=phoneno, emailvarificationdate=today, emailvarifaction=varification)
                else:
                    varification = "No"
                    code=random.randint(0000,999999)  
                    today = datetime.now()
                    print(today)
                    html_content = render_to_string("email.html",{"code":code,"name":fname})
                    text_content = strip_tags(html_content)
                    emailsend = EmailMultiAlternatives(
                    "Link FOR VERIFICATION",
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [email],
                    )
                    emailsend.attach_alternative(html_content,"text/html")
                    emailsend.send()
                    if password != '':
                        getpass = password.split(" ")
                        joinpass = "".join(getpass)
                        passwordUpdate = make_password(joinpass)
                        Customer.objects.filter(cid = obj).update(group=cgid, firstname=fname, lastname=lname, email=email, phoneno=phoneno, password=passwordUpdate, emailvarificationdate=today, emailvarifaction=varification, code=code, time=today)

                    else:
                        Customer.objects.filter(cid = obj).update(group=cgid, firstname=fname, lastname=lname, email=email, phoneno=phoneno, emailvarificationdate=today, emailvarifaction=varification, code=code, time=today)

                for i in post_dict['option']:
                    customerid = Customer.objects.latest('cid')
                    cid = Customer.objects.get(cid = customerid.cid)
                    aid = post_dict['option'][i].get('aid',None)
                    name = post_dict['option'][i]['name']
                    street = post_dict['option'][i]['street']
                    houseno = post_dict['option'][i]['houseno']
                    unitno = post_dict['option'][i]['unitno']
                    postalcode = post_dict['option'][i]['postalcode']
                    tag = post_dict['option'][i]['tag']
                    isdefault = post_dict['option'][i].get('isdefault', None)
                    if isdefault == 'on':
                            defaultval = "Yes"
                    else:
                        defaultval = "No"
                    city = post_dict['option'][i].get('city', None)
                    state = post_dict['option'][i].get('state')
                    
                    if aid == '' and cid == '' and name == '' and street == '' and houseno == '' and unitno == '' and postalcode == '' and tag == '' or city == '' and state == '':
                        messages.success(request," Update Successfully!")
                        return HttpResponseRedirect('/admin/Customer/customer/')  

                    if aid == '' or aid == None:
                        if city == '':
                            messages.success(request," Update Successfully!")
                            return HttpResponseRedirect('/admin/Customer/customer/')
                        else:   
                            cityid = City.objects.get(cityid = city)
                            sid = State.objects.get(stateid = state)
                            dataaddress = Address(customer=customerid, name=name, streetname=street, houseno=houseno, unitno=unitno, postalcode=postalcode, tag=tag, isdefault=defaultval, city=cityid ,state=sid)
                            dataaddress.save()                       

                    else:
                        cityid = City.objects.get(cityid = city)
                        sid = State.objects.get(stateid = state)
                        if defaultval == "Yes":
                            Address.objects.filter(isdefault="Yes").filter(customer = obj).update(isdefault="No")
                            Address.objects.filter(aid = aid).update(customer=customerid, name=name, streetname=street, houseno=houseno, unitno=unitno, postalcode=postalcode, tag=tag, isdefault=defaultval, city=cityid ,state=sid)

                        else:
                            Address.objects.filter(aid = aid).update(customer=customerid, name=name, streetname=street, houseno=houseno, unitno=unitno, postalcode=postalcode, tag=tag, isdefault=defaultval, city=cityid ,state=sid)

                messages.success(request," Update Successfully!")
                return HttpResponseRedirect('/admin/Customer/customer/')      
                
        return super(CustomerAdmin, self).changeform_view(request, obj, form_url, extra_context)

admin.site.register(CustomerGroup,CustomerGroupAdmin)
admin.site.register(Customer,CustomerAdmin)
# admin.site.register(Address)
# admin.site.register(City)
# admin.site.register(State)