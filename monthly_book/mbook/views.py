from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Stores, Products, Transactions
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from base64 import b64decode, b64encode
from .forms import AddStoreForm, AddProductForm
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File


# Error Success function
def view_error_success(request, args):
    error = ""
    if 'error' in request.session:
        error = request.session['error']
        del request.session['error']
        args["error"] = error
    success = ""
    if 'success' in request.session:
        success = request.session['success']
        del request.session['success']
        args["success"] = success
    return (request, args)


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        args = {}
        current_month = datetime.now().month
        current_year = datetime.now().year
        stores_count = Stores.objects.all().count()
        args["stores"] = stores_count
        products_count = Products.objects.all().count()
        args["products"] = products_count
        transactions_count = Transactions.objects.all().count()
        args["transactions"] = transactions_count
        total_txns_month = Transactions.objects.filter(txn_dop__month=current_month, txn_dop__year=current_year)
        total_txn_amt = 0.0
        for txn in total_txns_month:
            total_txns_month += txn.txn_amount
        args["total_txn_amt"] = total_txn_amt
        total_extra_txn_month = Transactions.objects.filter(txn_dop__month=current_month, txn_dop__year=current_year, product__product_is_extra=True)
        total_extra_amt = 0.0
        for extra_txn in total_extra_txn_month:
            total_extra_amt += extra_txn.txn_amount
        args["total_extra_amt"] = total_extra_amt
        return render(request, "index.html", args)
    else:
        return render(request, "index.html", {})

@login_required
def list_stores(request):
    if request.user.is_authenticated:
        stores = Stores.objects.all().order_by('store_name')
        args = {}
        args["stores"] = stores
        stores_form = AddStoreForm()
        args["stores_form"] = stores_form
        (request, args) = view_error_success(request, args)
        return render(request, "stores.html", args)
    else:
        return redirect('mbook:index')


@login_required
def add_store(request):
    if request.user.is_authenticated and request.method == "POST":
        stores_form = AddStoreForm(request.POST)
        if stores_form.is_valid():
            store = stores_form.save(commit=False)
            store.created_by = request.user
            store.save()
            request.session["success"] = "Store saved successfully!"
            return redirect('mbook:stores')
        else:
            request.session["error"] = stores_form.errors
            return redirect('mbook:stores')
    else:
        return redirect('mbook:index')


@login_required
def update_store(request, id):
    if request.user.is_authenticated:
        store = Stores.objects.get(id=id)
        if request.method == "GET":
            args = {}
            stores_form = AddStoreForm(initial={
                'store_name':store.store_name,
                'store_address':store.store_address,
                'store_type':store.store_type
            })
            args["stores_form"] = stores_form
            args["id"] = store.id
            (request, args) = view_error_success(request, args)
            return render(request, "edit_store.html", args)
        elif request.method == "POST":
            stores_form = AddStoreForm(request.POST, instance=store)
            if stores_form.is_valid():
                if not store.store_name == stores_form.cleaned_data.get('store_name'):
                    store.store_name = stores_form.cleaned_data.get('store_name')
                if not store.store_address == stores_form.cleaned_data.get('store_address'):
                    store.store_address = stores_form.cleaned_data.get('store_address')
                if not store.store_type == stores_form.cleaned_data.get('store_type'):
                    store.store_type = stores_form.cleaned_data.get('store_type')
                store.save()
                request.session["success"] = "{} - Store saved successfully!".format(store.store_name)
                return redirect('mbook:stores')
            else:
                request.session["error"] = stores_form.errors
                return redirect('mbook:stores')
        else:
            request.session["error"] = "{} - Method not allowed".format(request.method)
            return redirect('mbook:index')
    else:
        return redirect('mbook:index')


@login_required
def delete_store(request, id):
    if request.user.is_authenticated:
        try:
            Stores.objects.filter(id=id).delete()
            request.session["success"] = "Store Deleted Successfully"
            return redirect('mbook:stores')
        except:
            request.session["error"] = "Unable to delete the store"
            return redirect('mbook:stores')
    else:
        return redirect('mbook:index')


@login_required
def list_products(request):
    if request.user.is_authenticated:
        products = Products.objects.all().order_by('product_name')
        args = {}
        args["products"] = products
        products_form = AddProductForm()
        args["products_form"] = products_form
        (request, args) = view_error_success(request, args)
        return render(request, "products.html", args)
    else:
        return redirect('mbook:index')


@login_required
def add_product(request):
    if request.user.is_authenticated and request.method == "POST":
        products_form = AddProductForm(request.POST)
        if products_form.is_valid():
            product = products_form.save(commit=False)
            product.created_by = request.user
            product.save()
            request.session["success"] = "Product saved successfully!"
            return redirect('mbook:products')
        else:
            request.session["error"] = products_form.errors
            return redirect('mbook:products')
    else:
        return redirect('mbook:index')


@login_required
def update_product(request, id):
    if request.user.is_authenticated:
        product = Products.objects.get(id=id)
        if request.method == "GET":
            args = {}
            products_form = AddProductForm(initial={
                'product_name':product.product_name,
                'product_desc':product.product_desc,
                'product_qty':product.product_qty,
                'product_unit':product.product_unit,
                'product_code':product.product_code,
                'product_rate_per_unit':product.product_rate_per_unit,
                'product_ccy':product.product_ccy,
                'product_is_extra':product.product_is_extra
            })
            args["products_form"] = products_form
            args["id"] = product.id
            (request, args) = view_error_success(request, args)
            return render(request, "edit_product.html", args)
        elif request.method == "POST":
            products_form = AddProductForm(request.POST, instance=product)
            if products_form.is_valid():
                if not product.product_name == products_form.cleaned_data.get('product_name'):
                    product.product_name = products_form.cleaned_data.get('product_name')
                if not product.product_desc == products_form.cleaned_data.get('product_desc'):
                    product.product_desc = products_form.cleaned_data.get('product_desc')
                if not product.product_qty == products_form.cleaned_data.get('product_qty'):
                    product.product_qty = products_form.cleaned_data.get('product_qty')
                if not product.product_unit == products_form.cleaned_data.get('product_unit'):
                    product.product_unit = products_form.cleaned_data.get('product_unit')
                if not product.product_code == products_form.cleaned_data.get('product_code') or not product.product_barcode:
                    product.product_code = products_form.cleaned_data.get('product_code')
                    EAN = barcode.get_barcode_class('ean13')
                    product_barcode = EAN(product.product_code, writer=ImageWriter())
                    buffer = BytesIO()
                    product_barcode.write(buffer)
                    product.product_barcode.save(f"{product.product_code}.png", File(buffer), save=False)
                if not product.product_rate_per_unit == products_form.cleaned_data.get('product_rate_per_unit'):
                    product.product_rate_per_unit = products_form.cleaned_data.get('product_rate_per_unit')
                if not product.product_ccy == products_form.cleaned_data.get('product_ccy'):
                    product.product_ccy = products_form.cleaned_data.get('product_ccy')
                if not product.product_is_extra == products_form.cleaned_data.get('product_is_extra'):
                    product.product_is_extra = products_form.cleaned_data.get('product_is_extra')
                product.save()
                request.session["success"] = "{} - product saved successfully!".format(product.product_name)
                return redirect('mbook:products')
            else:
                request.session["error"] = products_form.errors
                return redirect('mbook:products')
        else:
            request.session["error"] = "{} - Method not allowed".format(request.method)
            return redirect('mbook:index')
    else:
        return redirect('mbook:index')


@login_required
def view_product(request, id):
    if request.user.is_authenticated:
        try:
            product = Products.objects.get(id=id)
            args = {}
            args["product"] = product
            (request, args) = view_error_success(request, args)
            return render(request, "view_product.html", args)
        except:
            request.session["error"] = "Unable to find the product"
            return redirect('mbook:products')
    else:
        return redirect('mbook:index')


@login_required
def delete_product(request, id):
    if request.user.is_authenticated:
        try:
            Products.objects.filter(id=id).delete()
            request.session["success"] = "Product Deleted Successfully"
            return redirect('mbook:products')
        except:
            request.session["error"] = "Unable to delete the product"
            return redirect('mbook:products')
    else:
        return redirect('mbook:index')


# User management views
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('mbook:index')
            else:
                request.session['error'] = "User is inactive!"
                return redirect("mbook:index")
        else:
            request.session['error'] = "Invalid Username / Password!"
            return redirect("mbook:index")
    else:
        return redirect("mbook:index")


def user_logout(request):
    logout(request)
    return redirect('mbook:index')