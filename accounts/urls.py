from django.urls import path
from . import views
# from store.views import product_list
app_name = 'accounts'

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("ordinarycustomer/", views.ordinary_customer_home, name="ordinary_customer_home"),
    path("wholesaler/", views.wholesaler_home, name="wholesaler_home"),
    # path("store/", product_list, name="product_list"),
]
