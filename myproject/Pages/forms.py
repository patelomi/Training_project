from dataclasses import fields
from pyexpat import model
from django import forms
from Pages.models import *

class PagesForm(forms.ModelForm):

    class Meta():
        model = Pages
        fields = ('slug','status','sortorder')