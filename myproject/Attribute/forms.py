from django import forms

from django.db import models
from Language.models import Language
from Attribute.models import *

selectinput = (
        ('Textbox', 'Textbox'),
        ('Radio', 'Radio'),
        ('Checkbox', 'Checkbox'),
        ('Boolean', 'Boolean'),
        ('Textarea', 'Textarea'),
        ('Multi-select', 'Multi-select'),
        ('Select', 'Select')
    )
class AttributeForm(forms.Form):
    class Meta:
        model = attribute
        fields = '__all__'
