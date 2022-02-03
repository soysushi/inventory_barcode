# adding uuid to allow users to have same username and name
import uuid
import json

from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from barcode import EAN13
from itertools import chain

from users.models import User
from .models import (
    Supplier,
    Recipient,
    Location,
    Section,
    Product,
    Order,
    Delivery,
    ProductVariant,
    ProductNumber
)
from .forms import (
    SupplierForm,
    RecipientForm,
    LocationForm,
    SectionForm,
    ProductForm,
    OrderForm,
    DeliveryForm,
)

from .helpers import (
    generate_label,
    print_label,
    generate_dropcode,
)

# Supplier views
@login_required(login_url='login')
def create_supplier(request):
    forms = SupplierForm()
    if request.method == 'POST':
        forms = SupplierForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(
                    username=email, password=password,
                    email=email, is_supplier=True
                )
                Supplier.objects.create(user=user, name=name, address=address)
                return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_supplier.html', context)


class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'


# Recipient views
@login_required(login_url='login')
def create_buyer(request):
    forms = RecipientForm()
    if request.method == 'POST':
        forms = RecipientForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(
                    username=email, password=password,
                    email=email, is_buyer=True
                )
                Recipient.objects.create(user=user, name=name, address=address)
                return redirect('buyer-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_buyer.html', context)


class RecipientListView(ListView):
    model = Recipient
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'


# Office views
@login_required(login_url='login')
def create_office(request):
    forms = LocationForm()
    if request.method == 'POST':
        forms = LocationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('office-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_office.html', context)


class LocationListView(ListView):
    model = Location
    template_name = 'store/office_list.html'
    context_object_name = 'office'


# Section views
@login_required(login_url='login')
def create_drop(request):
    forms = SectionForm()
    if request.method == 'POST':
        forms = SectionForm(request.POST)
        if forms.is_valid():
            forms.save()
            dropcode = ProductNumber.objects.get(name="dropcode")
            drop_temp = request.POST['name']
            drop = Section.objects.get(name=drop_temp)
            generate_dropcode(dropcode.number, drop)
            dropcode.number += 10
            dropcode.save()
            return redirect('drop-list')

    dropcode = ProductNumber.objects.get(name="dropcode")
    sortno = int(str(EAN13(str(dropcode.number))))
    forms.fields['sortno'].initial = sortno

    context = {
        'form': forms
    }
    return render(request, 'store/create_drop.html', context)


class SectionListView(ListView):
    model = Section
    template_name = 'store/drop_list.html'
    context_object_name = 'drop'


# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()

    if request.method == 'POST':
        forms = ProductForm(request.POST)
        # get product and product variant
        if forms.is_valid():
            forms.save()
            # get the response_objects
            response_objects = request.POST
            # get product instance
            product = Product.objects.get(
                sortno = request.POST['sortno']
            )
            # get product variants
            names = [v for k, v in request.POST.items() if k.startswith('variant_')]

            for name in names:
                ProductVariant.objects.create(
                    product=product,
                    variant=name,
                )
            # get the current barcode
            barcode = ProductNumber.objects.get(name="barcode")
            # product.sortno = barcode.number
            link = request.POST['link']
            generate_label(barcode.number, product, names, link)
            barcode.number += 10
            barcode.save()


            # get variants in POST request

            return redirect('product-list')
    # get the current barcodes
    barcode = ProductNumber.objects.get(name="barcode")
    sortno = int(str(EAN13(str(barcode.number))))
    forms.fields['sortno'].initial = sortno


    context = {
        'form': forms
    }
    return render(request, 'store/create_product.html', context)


#class ProductListView(ListView):
#    model = Product
#    template_name = 'store/product_list.html'
#    context_object_name = 'product'
@login_required(login_url='login')
def product_list(request):
    variants = []
    if request.method == 'POST':
        items = request.POST.getlist("product")
        print_label(items)
    products = Product.objects.all()
    for product in products:
         variants = product.productvariant_set.all()
    context = {
        'product': products,
        'variants': variants,
    }
    return render(request, 'store/product_list.html', context)


# Order views
@login_required(login_url='login')
def create_order(request):
    forms = OrderForm()
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            print("HELLO FORM IS VALID")
            product = forms.cleaned_data['product']
            buyer = forms.cleaned_data['buyer']
            instance = Order.objects.create(
                buyer=buyer,
                status='pending'
            )
            for items in product:
                instance.product.add(items)

            return redirect('order-list')

    context = {
        'form': forms
    }
    return render(request, 'store/create_order.html', context)

def search_products(request):
    if request.method=='POST':
        variants = []
        search_str_temp=json.loads(request.body).get('searchText')
        search_str = search_str_temp.split(", ")
        print([search_str[1:]])
        products=Product.objects.filter(variant__variant__in=search_str[1:]) & Product.objects.filter(name__contains=search_str[0])
        print(products)
        # for product in products:
            # variants = product.productvariant_set.all()
        data = products.values()
        res = {}
        for values in data:
                res.update({key: values[key] for key in values.keys()
                                   & {'id', 'sortno', 'name', 'label'}})


        print(res)
        return JsonResponse(res, safe=False)

class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context


# Delivery views
@login_required(login_url='login')
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_delivery.html', context)


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'store/delivery_list.html'
    context_object_name = 'delivery'
