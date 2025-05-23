
from django.urls import path
from . import views
app_name = 'main_page'

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('product/<str:name>', views.product_single, name='product_single'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('contact/', views.contact, name='contact'),
    path('order_succes/', views.order_succes, name='order_succes'),

]