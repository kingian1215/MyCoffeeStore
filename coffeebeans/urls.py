from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

# from store.views import product_list
app_name = 'coffeebeans'

urlpatterns = [
    # path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("users/", include("accounts.urls")),
    
    path('', views.product_list, name='product_list'),
    path('about/', views.about, name='about'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('register/', views.register, name='register'),
    # path('reservation/',make_reservation, name='make_reservation'),
    path('order_decrease/<int:order_id>/', views.order_decrease, name='order_decrease'),
    path('order_increase/<int:order_id>/', views.order_increase, name='order_increase'),
    path('order_delete/<int:order_id>/', views.order_delete, name='order_delete'),
    path('news/', views.news, name='news'),
]
