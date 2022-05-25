from django.shortcuts import render,redirect
from Language.models import *
from Pages.models import *
from .forms import PagesForm
# Create your views here.
listdata=[]
lan = Language.objects.all()
for i in lan:
    if i.isdefault == "Yes":
        languageid = i.title

def page_list():
    pages = Pages.objects.filter(status="Enabled").order_by('sortorder')
    return pages

def page_details(request,slug):
    if request.method == 'POST':
        sessiondata = request.POST.get('lang')
        request.session['data'] = sessiondata
        print("sessiondata: ",sessiondata)

    if request.session['data'] is None:
        request.session['data'] = languageid
        print("sessiondata: ",request.session['data'])
    
    pages = page_list()
    contentdata = PageLanguage.objects.all().values()
    language = Language.objects.all().values()
    pagedetails = PageLanguage.objects.raw("select * from pages_pagelanguage where pages_id = '"+slug+"'")
    print(pagedetails)

    return render(request,'admin/Pages/Home.html',{'contentdata':pagedetails,'pages':pages,"language":listdata,"datalist":request.session['data'],"language":language})