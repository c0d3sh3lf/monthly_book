# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings
from django.http import FileResponse

# Core and 3rd Party Imports
from datetime import date, datetime
from base64 import b64decode, b64encode
import barcode, os
from barcode.writer import ImageWriter
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

# Application Imports
from .models import Stores, Products, Transactions
from .forms import AddStoreForm, AddProductForm, AddTransactionForm


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


# Login Required Decorator
def login_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session["error"] = "You are not authenticated. Please authenticate yourself here."
            return redirect("mbook:index")
        else:
            return function(request, *args, **kwargs)
    return wrapper


# Create your views here.
def index(request):
    args = {}
    if request.user.is_authenticated:
        current_month = datetime.now().month
        current_year = datetime.now().year
        stores_count = Stores.objects.all().count()
        args["stores"] = stores_count
        products_count = Products.objects.all().count()
        args["products"] = products_count
        transactions_count = Transactions.objects.all().count()
        args["transactions"] = transactions_count
        total_txns_month = Transactions.objects.filter(txn_dop__month=current_month, txn_dop__year=current_year).all()
        total_txn_amt = 0.0
        for txn in total_txns_month:
            total_txn_amt += txn.txn_amount
        args["total_txn_amt"] = round(total_txn_amt, 2)
        total_extra_txn_month = Transactions.objects.filter(txn_dop__month=current_month, txn_dop__year=current_year, product__product_is_extra=True).all()
        total_extra_amt = 0.0
        for extra_txn in total_extra_txn_month:
            total_extra_amt += extra_txn.txn_amount
        args["total_extra_amt"] = round(total_extra_amt, 2)
        return render(request, "index.html", args)
    else:
        (request, args) = view_error_success(request, args)
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
                if not product.product_code == products_form.cleaned_data.get('product_code'):
                    product.product_code = products_form.cleaned_data.get('product_code')
                if not product.product_rate_per_unit == products_form.cleaned_data.get('product_rate_per_unit'):
                    product.product_rate_per_unit = products_form.cleaned_data.get('product_rate_per_unit')
                if not product.product_ccy == products_form.cleaned_data.get('product_ccy'):
                    product.product_ccy = products_form.cleaned_data.get('product_ccy')
                if not product.product_is_extra == products_form.cleaned_data.get('product_is_extra'):
                    product.product_is_extra = products_form.cleaned_data.get('product_is_extra')
                # Refreshing Barcode Image
                if product.product_barcode or os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(product.product_barcode))):
                    product.product_barcode.delete(save=False)
                product.product_code = products_form.cleaned_data.get('product_code')
                EAN = barcode.get_barcode_class('ean13')
                product_barcode = EAN(product.product_code, writer=ImageWriter())
                buffer = BytesIO()
                product_barcode.write(buffer)
                product.product_barcode.save(f"{product.product_code}.png", File(buffer), save=False)
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
        # try:
        product = Products.objects.get(id=id)
        args = {}
        args["product"] = product
        (request, args) = view_error_success(request, args)
        return render(request, "view_product.html", args)
        # except:
        #     request.session["error"] = "Unable to find the product"
        #     return redirect('mbook:products')
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


@login_required
def add_txn_pr(request, id):
    if request.user.is_authenticated:
        product = Products.objects.get(id=id)
        add_txn_pr_form = AddTransactionForm(initial={'product':product,
            'txn_product_code':product.product_code, 
            'txn_dop':date.today(),
            'txn_qty':product.product_qty,
            'txn_unit':product.product_unit,
            'txn_amount':product.product_rate_per_unit,
            'txn_ccy':product.product_ccy
            })
        args = {}
        args["add_txx_pr_form"] = add_txn_pr_form
        (request, args) = view_error_success(request, args)
        return render(request, "add_transaction.html", args)
    else:
        return redirect("mbook:index")


@login_required
def add_txn(request, ref):
    if request.user.is_authenticated:
        if request.method == "POST":
            add_txn_pr_form = AddTransactionForm(request.POST)
            if add_txn_pr_form.is_valid():
                product = add_txn_pr_form.cleaned_data.get('product')
                if add_txn_pr_form.cleaned_data.get('txn_product_code') != product.product_code and add_txn_pr_form.cleaned_data.get('txn_product_code') not in ['', '0', '0000000000000']:
                    product.product_code = add_txn_pr_form.cleaned_data.get('txn_product_code')
                    EAN = barcode.get_barcode_class('ean13')
                    product_barcode = EAN(product.product_code, writer=ImageWriter())
                    buffer = BytesIO()
                    product_barcode.write(buffer)
                    product.product_barcode.save(f"{product.product_code}.png", File(buffer), save=False)
                    product.save()
                txn = add_txn_pr_form.save(commit=False)
                txn.created_by = request.user
                txn.save()
                request.session["success"] = "Transaction Added Successfully."
                if ref == "prt":
                    return redirect("mbook:products")
                else:
                    return redirect("mbook:transactions")
            else:
                request.session["error"] = "Unable to add the transaction."
                if ref == "prt":
                    return redirect("mbook:products")
                else:
                    return redirect("mbook:transactions")
        else:
            request.session["error"] = f"{request.method} not allowed"
            return redirect("mbook:index")
    else:
        return redirect('mbook:index')


@login_required
def update_txn(request, id):
    if request.user.is_authenticated:
        transaction = Transactions.objects.get(id=id)
        if request.method == "GET":
            args = {}
            transactions_form = AddTransactionForm(initial={
                'store':transaction.store,
                'product':transaction.product,
                'txn_product_code':transaction.product.product_code,
                'txn_dop':transaction.txn_dop,
                'txn_qty':transaction.txn_qty,
                'txn_unit':transaction.txn_unit,
                'txn_amount':transaction.txn_amount,
                'txn_ccy':transaction.txn_ccy
            })
            args["transactions_form"] = transactions_form
            args["id"] = transaction.id
            (request, args) = view_error_success(request, args)
            return render(request, "edit_transaction.html", args)
        elif request.method == "POST":
            transactions_form = AddTransactionForm(request.POST, instance=transaction)
            if transactions_form.is_valid():
                if not transaction.store == transactions_form.cleaned_data.get('store'):
                    transaction.store = transactions_form.cleaned_data.get('store')
                if not transaction.product == transactions_form.cleaned_data.get('product'):
                    transaction.product = transactions_form.cleaned_data.get('product')
                if not transaction.txn_dop == transactions_form.cleaned_data.get('txn_dop'):
                    transaction.txn_dop = transactions_form.cleaned_data.get('txn_dop')
                if not transaction.txn_qty == transactions_form.cleaned_data.get('txn_qty'):
                    transaction.txn_qty = transactions_form.cleaned_data.get('txn_qty')
                product = transactions_form.cleaned_data.get('product')
                if transactions_form.cleaned_data.get('txn_product_code') != product.product_code and transactions_form.cleaned_data.get('txn_product_code') not in ['', '0', '0000000000000']:
                    product.product_code = transactions_form.cleaned_data.get('txn_product_code')
                    EAN = barcode.get_barcode_class('ean13')
                    product_barcode = EAN(product.product_code, writer=ImageWriter())
                    buffer = BytesIO()
                    product_barcode.write(buffer)
                    product.product_barcode.save(f"{product.product_code}.png", File(buffer), save=False)
                    product.save()
                if not transaction.txn_amount == transactions_form.cleaned_data.get('txn_amount'):
                    transaction.txn_amount = transactions_form.cleaned_data.get('txn_amount')
                if not transaction.txn_ccy == transactions_form.cleaned_data.get('txn_ccy'):
                    transaction.txn_ccy = transactions_form.cleaned_data.get('txn_ccy')
                if not transaction.txn_unit == transactions_form.cleaned_data.get('txn_unit'):
                    transaction.txn_unit = transactions_form.cleaned_data.get('txn_unit')
                transaction.save()
                request.session["success"] = "Transaction saved successfully!"
                return redirect('mbook:transactions')
            else:
                request.session["error"] = transactions_form.errors
                return redirect('mbook:transactions')
        else:
            request.session["error"] = "{} - Method not allowed".format(request.method)
            return redirect('mbook:index')
    else:
        return redirect('mbook:index')


@login_required
def view_txn(request, id):
    if request.user.is_authenticated:
        transaction = Transactions.objects.get(id=id)
        args = {}
        args["transaction"] = transaction
        (request, args) = view_error_success(request, args)
        return render(request, "view_transaction.html", args)
    else:
        return redirect('mbook:index')


@login_required
def delete_txn(request, id):
    if request.user.is_authenticated:
        try:
            Transactions.objects.filter(id=id).delete()
            request.session["success"] = "Transaction Deleted Successfully"
            return redirect('mbook:transactions')
        except:
            request.session["error"] = "Unable to delete the product"
            return redirect('mbook:transactions')
    else:
        return redirect('mbook:index')


@login_required
def list_transactions(request):
    if request.user.is_authenticated:
        transactions = Transactions.objects.all().order_by('-txn_dop')
        args = {}
        args["transactions"] = transactions
        add_txn_form = AddTransactionForm(initial={
            'txn_dop':date.today()
        })
        args["add_txn_form"] = add_txn_form
        (request, args) = view_error_success(request, args)
        return render(request, "transactions.html", args)
    else:
        return redirect('mbook:index')


@login_required
def reports(request):
    if request.user.is_authenticated:
        args = {}
        (request, args) = view_error_success(request, args)
        return render(request, "reports.html", args)
    else:
        return redirect("mbook:index")


@login_required
def generate_list_pdf(request):
    if request.user.is_authenticated:
        buffer = BytesIO()
        elements = []
        p = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=0.25*inch, rightMargin=0.25*inch, topMargin=0.25*inch, bottomMargin=0.25*inch)
        tStyle = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('BACKGROUND', (0, 30), (-1, 30), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 30), (-1, 30), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID',(0,1),(-1,-1),1,colors.black),
        ]) 

        unit_dict = {
            'KGS': 'KG',
            'LTR': 'L',
            'GMS': 'gms',
            'MIL': 'ml',
            'PKT': 'P',
            'PCS': 'Pcs.'
        }


        # Creating grocery table
        g_data = []
        grocery_regular_items = Products.objects.filter(product_is_extra=False, product_type="GRY")
        grocery_item_count = len(grocery_regular_items)
        counter = 1
        if grocery_item_count > 0:
            for grocery_counter in range(0, grocery_item_count, 2):
                if (counter-1) % 29 == 0:
                    g_data.append(['Sr. No.', 'R', 'P', 'Grocery Item', 'Item Qty.', '', 'Sr. No.', 'R', 'P', 'Grocery Item', 'Item Qty.'])
                try:
                    g_data.append([f"{counter}", "", "", f"{grocery_regular_items[grocery_counter].product_name}", f"{grocery_regular_items[grocery_counter].product_qty} {unit_dict[grocery_regular_items[grocery_counter].product_unit]}", "", f"{counter + int(grocery_item_count/2) + (grocery_item_count % 2 > 0)}", "", "", f"{grocery_regular_items[grocery_counter + 1].product_name}", f"{grocery_regular_items[grocery_counter + 1].product_qty} {unit_dict[grocery_regular_items[grocery_counter + 1].product_unit]}"])
                except IndexError:
                    g_data.append([f"{counter}", "", "", f"{grocery_regular_items[grocery_counter].product_name}", f"{grocery_regular_items[grocery_counter].product_qty} {unit_dict[grocery_regular_items[grocery_counter].product_unit]}", "", "", "", "", "", ""])
                counter += 1
            g_table = Table(g_data)
            g_table.setStyle(tStyle)
            elements.append(g_table)
            elements.append(PageBreak())

        # Creating Cosmetics / HouseHold Table
        # c_data = []
        # cosmetic_regular_items = Products.objects.filter(product_is_extra=False, product_type__in = ["CSM", "HLD"])
        # cosmetic_item_count = len(cosmetic_regular_items)
        # counter = 1
        # if cosmetic_item_count > 0:
        #     for cosmetic_counter in range(0, cosmetic_item_count, 2):
        #         if (counter-1) % 29 == 0:
        #             c_data.append(['Sr. No.', 'R', 'P', 'Cosmetic Item', 'Item Qty.', '', 'Sr. No.', 'R', 'P', 'Cosmetic Item', 'Item Qty.'])
        #         try:
        #             c_data.append([f"{counter}", "", "", f"{cosmetic_regular_items[cosmetic_counter].product_name}", f"{cosmetic_regular_items[cosmetic_counter].product_qty} {unit_dict[cosmetic_regular_items[cosmetic_counter].product_unit]}", "", f"{counter + int(cosmetic_item_count/2) + (cosmetic_item_count % 2 > 0)}", "", "", f"{cosmetic_regular_items[cosmetic_counter + 1].product_name}", f"{cosmetic_regular_items[cosmetic_counter + 1].product_qty} {unit_dict[cosmetic_regular_items[cosmetic_counter + 1].product_unit]}"])
        #         except IndexError:
        #             c_data.append([f"{counter}", "", "", f"{cosmetic_regular_items[cosmetic_counter].product_name}", f"{cosmetic_regular_items[cosmetic_counter].product_qty} {unit_dict[cosmetic_regular_items[cosmetic_counter].product_unit]}", "", "", "", "", "", ""])
        #         counter += 1
        #     c_table = Table(c_data)
        #     c_table.setStyle(tStyle)
        #     elements.append(c_table)
        #     elements.append(PageBreak())

        p.build(elements)
        buffer.seek(0)
        gen_datetime = datetime.now()
        filename = f"list_{gen_datetime.year}{gen_datetime.month}{gen_datetime.day}{gen_datetime.hour}{gen_datetime.minute}{gen_datetime.second}"
        return FileResponse(buffer, as_attachment=True, filename=filename)
    else:
        return redirect("mbook:index")


@login_required
def gen_month_txn(request):
    transactions = Transactions.objects.filter(txn_dop__month=datetime.now().month, txn_dop__year=datetime.now().year).order_by('txn_dop')
    buffer = BytesIO()

    pdf = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=0.25*inch, rightMargin=0.25*inch, topMargin=0.25*inch, bottomMargin=0.25*inch)

    elements = []    

    tStyle = TableStyle([
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
        ('ALIGN', (4, -1), (4, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black)
    ])

    tStyle_colspan = TableStyle([
        ('SPAN', (0, -1), (-1, -1)),
    ])

    unit_dict = {
            'KGS': 'KG',
            'LTR': 'L',
            'GMS': 'gms',
            'MIL': 'ml',
            'PKT': 'P',
            'PCS': 'Pcs.'
    }

    txn_data = []
    txn_count = len(transactions)
    counter = 1
    total_amount = 0.0
    ccy = ""
    if txn_count > 0:
        for transaction in transactions:
            if (counter - 1) == 0:
                txn_data.append([
                    "Sr. No.",
                    "Purchase Date",
                    "Purchased From",
                    "Item",
                    "Qty.",
                    "Amount.",
                ])
            txn_data.append([
                f"{counter}.",
                f"{(transaction.txn_dop).strftime('%b %d, %Y') }",
                f"{transaction.store.store_name}",
                f"{transaction.product.product_code} - {transaction.product.product_name}",
                f"{transaction.txn_qty} {unit_dict[transaction.txn_unit]}",
                "{} {:.2f}".format(transaction.txn_ccy, round(transaction.txn_amount, 2)),
            ])

            total_amount += transaction.txn_amount
            ccy = transaction.txn_ccy
            counter += 1

        total_amount = round(total_amount, 2)
        txn_data.append([
            "",
            "",
            "",
            "",
            "Grand Total:",
            "{} {:.2f}".format(ccy, total_amount)
        ])
        txns = Table(txn_data)
        txns.setStyle(tStyle)
        elements.append(txns)
    else:
        txn_data.append([
            "Sr. No.",
            "Purchase Date",
            "Purchased From",
            "Item",
            "Qty.",
            "Amount.",
        ])

        txn_data.append(["No Transactions found to list."])
        txns = Table(txn_data)
        txns.setStyle(tStyle)
        txns.setStyle(tStyle_colspan)
        elements.append(txns)


    pdf.build(elements)
    buffer.seek(0)
    filename = f"transactions_{datetime.now().year}{datetime.now().month}{datetime.now().day}{datetime.now().hour}{datetime.now().minute}{datetime.now().second}"
    return FileResponse(buffer, as_attachment=True, filename=filename)
        

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