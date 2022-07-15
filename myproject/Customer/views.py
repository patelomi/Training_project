from typing import final
from django.shortcuts import render,redirect
from Customer.models import *
from django.http import JsonResponse
from Customer.forms import *
from django.core import serializers
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.contrib import messages
import pytz
# Create your views here.

def deletedata(request):
    id = request.GET.get('id')
    i = Address.objects.get(aid = id[:-1])
    i.delete()
    return redirect("/admin/Customer/customer/")

def editdata(request):
    id = request.GET.get('id')
    aid = id.split("/")[0]
    senddata=[]
    i = Address.objects.get(aid = id[:-1])
    senddata.append(serializers.serialize('json',[i,]))
    return JsonResponse({'senddata':senddata,'aid':aid})

def emailvarification(request):
    code = request.GET.get("code")
    today = datetime.now()
    custdata = Customer.objects.filter(code = code)

    if custdata.count()>0:
        time = custdata[0].time
        finaltime = time + timedelta(minutes=1)
        now = pytz.utc.localize(today)
        if finaltime > now:
            Customer.objects.filter(code = code).update(emailvarifaction = "Yes",emailvarificationdate = today, code = "000000")
            return render(request,"email_varification.html")
        else:
            messages.add_message(request, messages.ERROR, 'Reset Time is expired')
            return HttpResponse("Time is Expired")

    else:
        messages.add_message(request, messages.ERROR, 'Reset code is expired')
        return HttpResponse("Code is Expired") 