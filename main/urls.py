from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    
    # Products Pages
    path('products/', views.show_products, name='show_products'),
    path('products/<int:id>/', views.show_product_detail, name='product_detail'),  # Add this line
    
    # JSON Endpoints
    path('json/', views.show_json, name='show_json'),
    path('json/my/', views.show_json_by_user, name='show_json_by_user'),
    
    # AJAX Endpoints for Product CRUD
    path('create-product-ajax/', views.create_product_ajax, name='create_product_ajax'),
    path('edit-product-ajax/<int:id>/', views.edit_product_ajax, name='edit_product_ajax'),
    path('delete-product-ajax/<int:id>/', views.delete_product_ajax, name='delete_product_ajax'),
]