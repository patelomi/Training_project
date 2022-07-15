from pyexpat import model
from django import forms
from Customer.models import *

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('group','firstname','lastname','profileimg','email','phoneno','password') 

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('aid', 'customer', 'name', 'streetname', 'houseno', 'unitno', 'postalcode', 'tag', 'city' , 'state', 'isdefault') 