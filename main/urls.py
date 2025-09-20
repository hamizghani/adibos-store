from django.urls import path
from main.views import *
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('products/', show_products, name='show_products'),
    path('products/<int:id>/', show_product_detail, name='show_product_detail'),
    path('products/add/', add_product, name='add_product'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
]
# http://localhost:8000/xml
# http://localhost:8000/json
# http://localhost:8000/xml/1/
# http://localhost:8000/json/1/