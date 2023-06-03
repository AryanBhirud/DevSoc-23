from django import forms
from .models import *

class priceForm(forms.Form):
    price = forms.CharField(label='price', required=True)
