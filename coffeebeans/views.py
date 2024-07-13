from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem,Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from decimal import Decimal

# Create your views here.

def index(request):
    return render(request, 'index.html')


def product_list(request):
    products = Product.objects.all()
    image_range = range(10001, 10014)
  
    discounted_products = [
        {
            'product': product,
            'discounted_price': int(product.price * Decimal('0.9'))
        } for product in products
    ]
    print(discounted_products)

    context = {
        'discounted_products': discounted_products,
        # 'is_wholesaler': request.user.is_wholesaler if request.user.is_authenticated else False,
        'products': products,
        'image_range': image_range,
    }
    return render(request, 'coffeebeans/product_list.html',  context)

def about(request):
    return render(request, 'coffeebeans/about.html')

@login_required(login_url='/users/login/') #檢查是否登入,若已登入才會執行add_to_cart()
def add_to_cart(request, product_id):
    # product = Product.objects.get(id=product_id)

    # product = get_object_or_404(Product, id=product_id)
    # cart, created = Cart.objects.get_or_create(user=request.user)
    # cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    # # cart_item.quantity += 1
    # quantity = int(request.POST.get('quantity', 1))
    # print(quantity)
    # # 檢查購物車中是否已經有這個商品，如果有則更新數量，否則創建新的購物車項目
    # cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    # cart_item.quantity += quantity  # 增加數量
    # cart_item.save()
    
    # return redirect('coffeebeans:product_list')

    # 以下為修改後的程式碼，可增加購物車商品數量功能
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # 獲取表單提交的數量，默認為1
        quantity = int(request.POST.get('quantity', 1))
        
        # 檢查購物車中是否已經有這個商品，如果有則更新數量，否則創建新的購物車項目
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity  # 增加數量
        cart_item.save()
    
    return redirect('coffeebeans:product_list')

@login_required(login_url='/users/login/')
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        # cart_items = cart.cartitem_set.all()
        if not cart_items.exists():
                message = "購物車現在是空的"
                total_price = 0
        else:
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            message = ""
    
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total_price = 0
        message = "購物車現在是空的"

    return render(request,'coffeebeans/view_cart.html', {
        'cart':cart, 
        'cart_items': cart_items,
        'total_price':total_price, 
        'message': message
        })

@login_required(login_url='/users/login/')
# def checkout(request):
#     try:
#         cart = Cart.objects.get(user=request.user)
#         cart_items = cart.items.all()
#         if not cart_items.exists():
#                 message = "購物車現在是空的"
#                 total_price = 0
#         else:
#             total_price = sum(item.product.price * item.quantity for item in cart_items)
#             message = ""
#             if request.method == 'POST':
#                 # 模擬實際的付款流程，寫入資料庫
#                 order = Order.objects.create(user=request.user, total_price=total_price)
#                 order.save()
#                 for item in cart_items:
#                     OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
#                 cart.items.all().delete()
#                 return redirect('coffeebeans:order_success') # 導向訂單成功頁面

#     except Cart.DoesNotExist:
#         cart = None
#         cart_items = []
#         total_price = 0
#         message = "購物車現在是空的"
    
#     return render(request,'coffeebeans/checkout.html', {'cart':cart, 'total_price':total_price, 'message': message})
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        if not cart_items.exists():
            message = "購物車現在是空的"
            total_price = 0
        else:
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            message = ""
            if request.method == 'POST':
                # 創建訂單實例
                order = Order(user=request.user)
                order.save()  # 首先保存 order，這樣它會有一個主鍵

                # 然後創建 OrderItem 實例
                for item in cart_items:
                    OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                
                # 最後更新並保存總價
                order.total_price = order.calculate_total_price()
                order.save()

                # 清空購物車
                cart.items.all().delete()
                return redirect('coffeebeans:order_success')  # 導向訂單成功頁面

    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total_price = 0
        message = "購物車現在是空的"
    
    return render(request, 'coffeebeans/checkout.html', {'cart': cart, 'total_price': total_price, 'message': message})

@login_required(login_url='/users/login/')
def order_success(request):
    return render(request,'coffeebeans/order_success.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('coffeebeans:product_list')  # 註冊成功後導向商品列表頁面
    else:
        form = UserCreationForm()
    return render(request, 'coffeebeans/register.html', {'form': form})

@login_required(login_url='/users/login/')
def order_increase(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='Pending')
    order.quantity += 1
    order.save()
    return redirect('coffeebeans:order_confirmation', order_id=order.id)

@login_required(login_url='/users/login/')
def order_decrease(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='Pending')
    if order.quantity > 1:
        order.quantity -= 1
        order.save()
    return redirect('coffeebeans:order_confirmation', order_id=order.id)

@login_required(login_url='/users/login/')
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='Pending')
    order.delete()
    return redirect('coffeebeans:order_confirmation', order_id=order_id)

def news(request):
    return render(request, 'coffeebeans/news.html')