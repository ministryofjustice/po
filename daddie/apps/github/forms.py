from django import forms

from models import Product


class AddRepoToProductForm(forms.Form):
    product_id = forms.ModelChoiceField(queryset=Product.objects.all())
