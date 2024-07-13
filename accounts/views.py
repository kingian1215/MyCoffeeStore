from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from.forms import CustomUserCreationForm, CustomAuthenticationForm 
from .decorators import Wholesaler_required
from django import forms

# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = True #false 用戶註冊後需管理員審核後才能登入
#             user.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('product_list')
#             # return redirect('login')
#     else:
#         form = CustomUserCreationForm()
        
#     return render(request, 'register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        profile_form = CustomUserCreationForm(request.POST)
        if profile_form.is_valid():
            # print(form.cleaned_data)
            # print(profile_form.cleaned_data)
            # user = form.save()

            user_type = profile_form.cleaned_data.get('user_type')
            
            # user = form.save(commit=False)
            # user.email = profile_form.cleaned_data.get('email')
            # user.save()
            profile = profile_form.save(commit=False)
            # profile.user = user
            profile.save()

            # 讀取表單內容並登錄用戶
            username = profile_form.cleaned_data.get('username')
            password = profile_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            # print(f"Username: {username}")
            # print(f"Password: {password}")
            # print(f"Authenticated User: {user}")

            login(request, user)
            
            # return redirect('index')
            if user_type=="is_Wholesaler":
                return redirect('accounts:wholesaler_home')
            elif user_type=="is_OrdinaryCustomer":
                return redirect('accounts:ordinary_customer_home')
            else:
                return redirect('coffeebeans:index')
    else:
        # print(form.errors)
        # print(profile_form.errors)
        form = UserCreationForm()
        profile_form = CustomUserCreationForm()
    return render(request, 'register.html', {'profile_form': profile_form})
                  
    # if request.method == 'POST':
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)  # 暫時不保存用戶，稍後再保存
    #         user.is_active = True #false 用戶註冊後需管理員審核後才能登入
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password1')
    #         user.set_password(password)  # 加密密碼
    #         user.save()  # 保存用戶到數據庫中

    #         # 認證用戶
    #         print(f"Username: {username}")
    #         print(f"Password: {password}")

    #         user = authenticate(username=username, password=password)
    #         print(f"Authenticated User: {user}")

    #         if user is not None:
    #             login(request, user)
    #             return redirect('index')
    #         else:
    #             print("Authentication failed.")
    #             return render(request, 'register.html', {
    #                 'form': form,
    #                 'error_message': '註冊成功，但認證失敗。請聯繫管理員。'
    #             })
    # else:
    #     form = CustomUserCreationForm()

    # return render(request, 'register.html', {'form': form})

def login_view(request):
    print("Login view called")
    if request.method == 'POST':
        print("POST request received")
        form = CustomAuthenticationForm(request, data=request.POST)
        # 驗證表單
        try:
            if form.is_valid():
                print("Form is valid")
                # 認證成功
                user = form.get_user()
                print(f"Authenticated User: {user}")
                if user.is_approved:
                    # 登入成功is_approved
                    login(request, user)
                    if user.is_Wholesaler:
                        return redirect('accounts:wholesaler_home')
                    elif user.is_OrdinaryCustomer:
                        return redirect('accounts:ordinary_customer_home')
                    else:
                        return redirect('coffeebeans:product_list')
                else:
                    print('您的帳號尚未通過審核，請聯繫管理員')
                    return render(request, 'login.html', {'form': form, 'error': '您的帳號尚未通過審核，請聯繫管理員'})
            else:
                print('表單驗證失敗:', form.errors)
                return render(request, 'login.html', {'form': form, 'error': '帳號或密碼輸入錯誤，請檢查後重新再試一次'})
        except forms.ValidationError as e:
            print(f'Validation error: {e}')
            return render(request, 'login.html', {'form': form, 'error': str(e)})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request) #登出
    return redirect('coffeebeans:product_list')

# @login_required(login_url='/login/')
def ordinary_customer_home(request):
    return render(request, 'OrdinaryCustomer_home.html')


# @login_required(login_url='/login/')
# @Wholesaler_required
def wholesaler_home(request):
    return render(request, 'Wholesaler_home.html')