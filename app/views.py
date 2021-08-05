from django import forms
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models
from django.db.models.query import RawQuerySet
from django.shortcuts import render
from django.views import View
from .models import (
    CATEGORY_CHOICES,
    Product,
    Customer,
    Cart, 
    OrderPlaced
    )
from .forms import CustomerRegistrationForm, CustomeProfileForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        total_item = 0
        topwears = Product.objects.filter(category="TP")
        bottomwears = Product.objects.filter(category="BW")
        mobiles = Product.objects.filter(category="M")
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        return render(request, "app/home.html", {"topwears" : topwears, "bottomwears" : bottomwears, "mobiles" : mobiles, 'items' : total_item})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        total_item = 0
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists() 
            total_item = len(Cart.objects.filter(user=request.user))
        return render(request, "app/productdetail.html", {"product" : product, 'item_exists' : item_already_in_cart, 'items' : total_item})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

@login_required
def add_to_cart(request):
    user = request.user
    total_item = 0
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    reg = Cart(user=user, product=product)
    reg.save()
    if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
    return redirect('/cart', {'items' : total_item})

def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', { 'active' : 'btn-primary', 'add' : add})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    total_items = 0
    if request.user.is_authenticated: 
        total_items = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', { 'order_placed' : op, 'items' : total_items })

def mobile(request, data=None):
    total_items = 0
    if data == None:
        mobiles = Product.objects.filter(category="M")
        if request.user.is_authenticated: 
            total_items = len(Cart.objects.filter(user=request.user))
    elif data == "Xiaomi" or data == "Samsung":
        mobiles = Product.objects.filter(category="M").filter(brand=data)
        if request.user.is_authenticated: 
            total_items = len(Cart.objects.filter(user=request.user))
    elif data == "below":
        mobiles = Product.objects.filter(category="M").filter(selling_price__lt=10000)
        if request.user.is_authenticated: 
            total_items = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html', {"mobiles" : mobiles, 'items' : total_items})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form' : form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'app/customerregistration.html', {'form' : form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    total_item = 0
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0 
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for prod in cart_product:
            temp_amount = ((prod.quantity) * (prod.product.selling_price - prod.product.discounted_price))
            amount += temp_amount
    if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html', { 'add' : add , 'total_amount' : amount + shipping_amount, 'cart_items' : cart_items, 'items' : total_item})

@method_decorator(login_required, name='dispatch')
class ProfileView(View): 
    def get(self, request):
        form = CustomeProfileForm()
        total_item = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        return render(request, "app/profile.html", {'form' : form, 'active' : 'btn-primary', 'items' : total_item})
    
    def post(self, request):
        form = CustomeProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulation! Profile Updated Successfully")
        return render(request, "app/profile.html", {'form' : form, 'active' : 'btn-primary'})

@login_required  
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user  == user]
        total_item = 0
        total_item = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * (p.product.selling_price - p.product.discounted_price))
                amount += temp_amount
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts' : cart, 'amount' : amount, 'shipping_price' : shipping_amount, 'total' : total_amount, 'items' : total_item})
        else: 
            return render(request, 'app/emptycart.html', { 'items' : total_item } )

def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user  == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * (p.product.selling_price - p.product.discounted_price))
            amount += temp_amount
            
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'total' : amount + shipping_amount
        }

        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user  == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * (p.product.selling_price - p.product.discounted_price))
            amount += temp_amount
            
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'total' : amount + shipping_amount
        }

        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user  == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * (p.product.selling_price - p.product.discounted_price))
            amount += temp_amount
            
        data = {
            'amount' : amount,
            'total' : amount + shipping_amount
        }

        return JsonResponse(data)

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("/orders/")