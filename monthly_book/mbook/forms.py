from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.forms import fields, widgets
from django.forms.models import ModelForm
from .models import Stores, Products, Transactions

class AddStoreForm(forms.ModelForm):

    store_name = forms.CharField(max_length=512, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ABC Company'
    }), label="Store Name")

    store_address = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Address'
    }), label="Store Address / Website")

    store_type = forms.ChoiceField(choices=[
        ('LCL','Local'),
        ('ONL', 'Online'),
    ], required=True, widget=forms.Select(attrs={
        'class':'form-control',
    }), label="Store Type")

    class Meta:
        model = Stores
        fields = ('store_name', 'store_address', 'store_type')

    def save(self, commit=True):
        store = super(AddStoreForm, self).save(commit=False)
        if commit:
            store.save()
        return store



class AddProductForm(forms.ModelForm):
    
    product_name = forms.CharField(max_length=512, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Cadbury Dairy Milk'
    }), label="Product Name")

    product_desc = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Product Description'
    }), label="Description")

    product_qty = forms.FloatField(required=True, widget=forms.NumberInput(attrs={
        'class':'form-control',
        'placeholder':'Quantity'
    }), label="Product Quantity")

    product_unit = forms.ChoiceField(choices=[
        ('KGS','Kilogram'),
        ('LTR', 'Litres'),
        ('GMS', 'Grams'),
        ('MIL', 'Millilitres'),
        ('PKT', 'Packet'),
        ('PCS', 'Pieces')
    ], required=True, widget=forms.Select(attrs={
        'class':'form-control',
    }), label="Product Unit")

    product_code = forms.CharField(max_length="191", required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Product Barcode'
    }), label="Product Code")

    product_rate_per_unit = forms.FloatField(required=True, widget=forms.NumberInput(attrs={
        'class':'form-control',
        'placeholder':'Rate per Unit'
    }), label="Product Rate")

    product_ccy = forms.ChoiceField(choices=[
        ('AED','United Arab Dirhams'),
        ('USD', 'United State Dollars'),
        ('INR', 'Indian Rupees'),
        ('GBP', 'Great Britain Pounds'),
        ('EUR', 'Euros')
    ], required=True, widget=forms.Select(attrs={
        'class':'form-control',
    }), label="Product Currency")

    product_is_extra = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class':'form-control',
        'value':'Extra Item?'
    }), label="Extra Item?")

    class Meta:
        model = Products
        fields = ('product_name', 'product_desc', 'product_qty', 'product_unit', 'product_code', 'product_rate_per_unit', 'product_ccy', 'product_is_extra')

    def save(self, commit=True):
        product = super(AddProductForm, self).save(commit=False)
        if commit:
            product.save()
        return product