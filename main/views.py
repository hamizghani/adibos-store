from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core import serializers
from .models import Product
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
def show_main(request):
    context = {
        'app_name' : 'Adibos Store',
        'name': 'Muhammad Hamiz Ghani Ayusha',
        'class': 'PBP C',
        'user_logged_in': request.user.username,
        'last_login': request.COOKIES.get('last_login'),
    }

    return render(request, "main.html", context)

@login_required(login_url='/login')
def show_products(request):
    products = Product.objects.filter(owner=request.user)
    context = {
        "products": products,
    }
    return render(request, "product_list.html", context)

@login_required(login_url='/login')
def show_product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {
        "product": product,
    }
    return render(request, "product_detail.html", context)

@login_required(login_url='/login')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, 'Produk berhasil ditambahkan!')
            return redirect("main:show_products")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id, owner=request.user)
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diupdate!')
            return redirect('main:show_products')
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product': product}
    return render(request, "edit_product.html", context)

@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, owner=request.user)
    product.delete()
    messages.success(request, 'Produk berhasil dihapus!')
    return redirect('main:show_products')

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response 

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response