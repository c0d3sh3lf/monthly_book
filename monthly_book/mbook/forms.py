from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.forms import fields, widgets
from django.forms.models import ModelForm
from .models import Stores, Products, Transactions
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from .widgets import DatePickerInput
from datetime import date

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

    product_code = forms.CharField(max_length="13", required=False, widget=forms.NumberInput(attrs={
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

    product_type = forms.ChoiceField(choices=[
        ('GRY','Grocery'),
        ('CSM', 'Cosmetics'),
        ('VLF', 'Vegetables / Leaves / Fruits'),
        ('ESS', 'Essentials'),
        ('HLD', 'Household'),
        ('OTH', 'Others')
    ], required=True, widget=forms.Select(attrs={
        'class':'form-control',
    }), label="Product Type")

    product_is_extra = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class':'form-control',
        'value':'Extra Item?'
    }), label="Extra Item?")

    class Meta:
        model = Products
        fields = ('product_name', 'product_desc', 'product_qty', 'product_unit', 'product_code', 'product_rate_per_unit', 'product_ccy', 'product_type', 'product_is_extra')

    def save(self, commit=True):
        product = super(AddProductForm, self).save(commit=False)
        if product.product_code and (product.product_code != "0" or product.product_code != '' or product.product_code != '0000000000000'):
            EAN = barcode.get_barcode_class('ean13')
            product_barcode = EAN(product.product_code, writer=ImageWriter())
            buffer = BytesIO()
            product_barcode.write(buffer)
            product.product_barcode.save(f"{product.product_code}.png", File(buffer), save=False)
        else:
            product.product_code = "0000000000000"
            EAN = barcode.get_barcode_class('ean13')
            product_barcode = EAN(product.product_code, writer=ImageWriter())
            buffer = BytesIO()
            product_barcode.write(buffer)
            product.product_barcode.save(f"{product.product_code}.png", File(buffer), save=False)
        if commit:
            product.save()
        return product


class AddTransactionForm(forms.ModelForm):

    store = forms.ModelChoiceField(queryset=Stores.objects.all().order_by("store_name"), widget=forms.Select(attrs={
        'class':'form-control'
    }), label="Store")

    product = forms.ModelChoiceField(queryset=Products.objects.all().order_by("product_name"), widget=forms.Select(attrs={
        'class':'form-control'
    }), label="Product")

    txn_product_code = forms.CharField(max_length="13", required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Product Barcode'
    }), label="Product Code")

    txn_dop = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=DatePickerInput(attrs={
        'class':'form-control',
        'max-date': date.today()
    }), label="Date of Purchase")

    txn_qty = forms.FloatField(required=True, widget=forms.NumberInput(attrs={
        'class':'form-control',
        'placeholder':'Quantity'
    }), label="Transaction Quantity")

    txn_unit = forms.ChoiceField(choices=[
        ('KGS','Kilogram'),
        ('LTR', 'Litres'),
        ('GMS', 'Grams'),
        ('MIL', 'Millilitres'),
        ('PKT', 'Packet'),
        ('PCS', 'Pieces')
    ], required=True, widget=forms.Select(attrs={
        'class':'form-control',
    }), label="Product Unit")

    txn_amount = forms.FloatField(required=True, widget=forms.NumberInput(attrs={
        'class':'form-control',
        'placeholder':'Rate per Unit'
    }), label="Transaction Amount")

    txn_ccy = forms.ChoiceField(choices=[
        ('AED','United Arab Dirhams'),
        ('USD', 'United State Dollars'),
        ('INR', 'Indian Rupees'),
        ('GBP', 'Great Britain Pounds'),
        ('EUR', 'Euros')
    ], required=True, widget=forms.Select(attrs={
        'class':'form-control',
    }), label="Product Currency")

    class Meta:
        model = Transactions
        fields = ('store', 'product', 'txn_product_code', 'txn_dop', 'txn_qty', 'txn_unit', 'txn_amount', 'txn_ccy')

    def save(self, commit=True):
        txn = super(AddTransactionForm, self).save(commit=False)
        if commit:
            txn.save()
        return txn