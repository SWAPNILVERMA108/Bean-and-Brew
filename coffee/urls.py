
from django.urls import path
from . import views


# localhost:8000/chai/
# localhost:8000/chai/order/

urlpatterns = [
    path('',views.coffee,name='coffee'),
    path('stores/', views.coffee_stores_view, name='coffee_stores'),
    path('order/', views.order_create, name='order_create'),
    path('orders/', views.my_orders, name='my_orders'),
    path('store-orders/', views.store_orders, name='store_orders'),
    path('<int:coffee_id>/',views.coffee_detail,name='coffee_detail'),
]
