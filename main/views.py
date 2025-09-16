from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core import serializers
from .models import Product
from .forms import ProductForm

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

def show_main(request):
    context = {
        'app_name' : 'Adibos Store',
        'name': 'Muhammad Hamiz Ghani Ayusha',
        'class': 'PBP C'
    }

    return render(request, "main.html", context)

def show_products(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "product_list.html", context)

def show_product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {
        "product": product,
    }
    return render(request, "product_detail.html", context)

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:show_products")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

