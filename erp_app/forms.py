from django import forms
from .models import *
class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Rechercher un produit')