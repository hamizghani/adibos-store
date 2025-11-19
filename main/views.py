from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import datetime
from .forms import StudentForm
import json

from .forms import ProductForm
from .models import Product, Student

# Login View dengan AJAX
def login(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful!',
                    'user': username
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid username or password'
                }, status=401)
        else:
            # Handle regular form submission
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                auth_login(request, user)
                return redirect('main:show_main')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# def create_student(request):
#     student = Student.objects.create('Ghani', 2024, 'mahasiswa 2024')
#     return render('show_student.html', {'student' : student})

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:show_student")
    else:
        form = StudentForm()
    return render(request, "student_form.html", {"bambang": form})

# Register View dengan AJAX
def register(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Registration successful!',
                    'user': user.username
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Registration failed',
                    'errors': form.errors
                }, status=400)
        else:
            # Handle regular form submission
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been created! You can now log in.')
                return redirect('main:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

# Logout View dengan Toast
@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('main:login')

# Show JSON - Return semua products
@login_required(login_url='/login')
def show_json(request):
    products = Product.objects.all()
    return HttpResponse(serializers.serialize('json', products), content_type='application/json')

# Show JSON by User - Return products milik user saja
@login_required(login_url='/login')
def show_json_by_user(request):
    products = Product.objects.filter(owner=request.user)
    return HttpResponse(serializers.serialize('json', products), content_type='application/json')

# Create Product AJAX
@login_required(login_url='/login')
@require_POST
def create_product_ajax(request):
    try:
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        thumbnail = request.POST.get('thumbnail')
        category = request.POST.get('category')
        is_featured = request.POST.get('is_featured') == 'on'
        
        # Validasi
        if not name or not price or not description or not thumbnail or not category:
            return JsonResponse({
                'status': 'error',
                'message': 'All fields are required'
            }, status=400)
        
        # Validasi price
        try:
            price = int(price)
            if price < 0:
                raise ValueError("Price cannot be negative")
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'Price must be a valid positive number'
            }, status=400)
        
        # Create product
        product = Product.objects.create(
            owner=request.user,
            name=name,
            price=price,
            description=description,
            thumbnail=thumbnail,
            category=category,
            is_featured=is_featured
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product created successfully!',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'thumbnail': product.thumbnail,
                'category': product.category,
                'is_featured': product.is_featured,
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# Edit Product AJAX
@login_required(login_url='/login')
@require_POST
def edit_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id, owner=request.user)
        
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        thumbnail = request.POST.get('thumbnail')
        category = request.POST.get('category')
        is_featured = request.POST.get('is_featured') == 'on'
        
        # Validasi
        if not name or not price or not description or not thumbnail or not category:
            return JsonResponse({
                'status': 'error',
                'message': 'All fields are required'
            }, status=400)
        
        # Validasi price
        try:
            price = int(price)
            if price < 0:
                raise ValueError("Price cannot be negative")
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'Price must be a valid positive number'
            }, status=400)
        
        # Update product
        product.name = name
        product.price = price
        product.description = description
        product.thumbnail = thumbnail
        product.category = category
        product.is_featured = is_featured
        product.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product updated successfully!',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'thumbnail': product.thumbnail,
                'category': product.category,
                'is_featured': product.is_featured,
            }
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found or you do not have permission to edit it'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# Delete Product AJAX
@login_required(login_url='/login')
@require_POST
def delete_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id, owner=request.user)
        product_name = product.name
        product.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Product "{product_name}" deleted successfully!'
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found or you do not have permission to delete it'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# Show Products Page
@login_required(login_url='/login')
def show_products(request):
    context = {
        'name': request.user.username,
    }
    return render(request, 'product_list.html', context)

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