# from django.shortcuts import render,redirect
# from Language.models import *
# from Pages.models import *
# from .forms import PagesForm
# # Create your views here.

# listdata=[]
# #getting data from language table
# lan = Language.objects.all()
# for i in lan:
#     if i.isdefault == "Yes":
#         languageid = i.title

# #filter via enabal
# def page_list():
#     pages = Pages.objects.filter(status="Enabled").order_by('sortorder')
#     return pages

# #geting slug into the database
# def page_details(request,slug):

#     #passing the language in session
#     if request.method == 'POST':
#         sessiondata = request.POST.get('lang')
#         request.session['data'] = sessiondata
#         print("sessiondata: ",sessiondata)

#     if request.session['data'] is None:
#         request.session['data'] = languageid
#         print("sessiondata: ",request.session['data'])
    
#     pages = page_list()
#     contentdata = PageLanguage.objects.all().values()
#     language = Language.objects.all().values()
#     pagedetails = PageLanguage.objects.raw("select * from pages_pagelanguage where pages_id = '"+slug+"'")
#     print(pagedetails)

#     return render(request,'admin/Pages/Home.html',{'contentdata':pagedetails,'pages':pages,"language":listdata,"datalist":request.session['data'],"language":language})


# # <table class="optiontable" id="optiontable">
# #     <tr>
# #                     {% for i in lang_data %}
# #                     <th>Name [{{i.locale}}]</th>
# #                     {% endfor %}
# #                     <th>Custom Option</th>
# #                     <th>Sort Order</th>
# #                     <th>Default?</th>
# #                     <th>Delete</th>
# #                 </tr>
# #                 <tr>
# #                     {% for i in lang_data %}
# #                     {% for data in opt_data %}
# #                     {% if i.locale == data.language_id %}
# #                     <input type="hidden" value="{{i.locale}}" name="option{{i.locale}}[oplanguage]"
# #                         id="option{{i.locale}}[oplanguage]" required>
# #                     <td><input type="text" name="option{{i.locale}}[opname]" id="option{{i.locale}}[opname]"
# #                             value="{{data.name}}" required></td>
# #                     {% endif %}
# #                     {% endfor %}
# #                     {% endfor %}
# #                     {% for i in option_data %}
# #                     <td><input type="text" name="option[option]" id="option[option]" value="{{i.coustomoption}}"
# #                             required></td>
# #                     <td><input type="text" name="option[order]" id="option[order]" value="{{i.sortorder}}" required>
# #                     </td>
# #                     <td><select>
# #                             <option disabled selected>------</option>
# #                             <option selected value="{{i.default}}">{{i.default}}</option>
# #                         </select></td>
# #                     <td><input type="button" onclick="deletedata()" value="delete" style="background-color: #a41515;">
# #                     </td>
# #                     {% endfor %}
# #             </table>