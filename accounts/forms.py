from django import forms
from.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    user_type = forms.ChoiceField(
        choices=[
            ('is_OrdinaryCustomer', '普通顧客'),
            ('is_Wholesaler', '批發商')
        ],
        widget=forms.RadioSelect,
        label="用戶類型"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type','address', 'phone', 'email')

    def clean(self):
        cleaned_data = super().clean()
        # print("cleaned_data",cleaned_data)

        user_type = cleaned_data.get('user_type')
        # is_OrdinaryCustomer = cleaned_data.get('is_OrdinaryCustomer')
        # is_Wholesaler = cleaned_data.get('is_Wholesaler')
        # print("user_type",user_type)

        if user_type == 'is_OrdinaryCustomer':
            cleaned_data['is_OrdinaryCustomer'] = True
            cleaned_data['is_Wholesaler'] = False
        elif user_type == 'is_Wholesaler':
            cleaned_data['is_OrdinaryCustomer'] = False
            cleaned_data['is_Wholesaler'] = True
        else:
            print("error")
            raise forms.ValidationError("必須選擇一個選項：普通顧客或批發商。")
        
        # if is_OrdinaryCustomer and is_Wholesaler:
        #     raise forms.ValidationError("只能選擇一個選項：普通顧客或批發商。")
        # if not is_OrdinaryCustomer and not is_Wholesaler:
        #     raise forms.ValidationError("必須選擇一個選項：普通顧客或批發商。")
        print("cleaned_data",cleaned_data)
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_OrdinaryCustomer = self.cleaned_data['is_OrdinaryCustomer']
        user.is_Wholesaler = self.cleaned_data['is_Wholesaler']
        if commit:
            user.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        print("Starting clean method")
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # is_approved = CustomUser.objects.get(username=username).is_approved
        # is_Wholesaler = CustomUser.objects.get(username=username).is_Wholesaler
        # is_OrdinaryCustomer = CustomUser.objects.get(username=username).is_OrdinaryCustomer

        if username is None or password is None:
            raise forms.ValidationError('請輸入用戶名和密碼')
        
        try:
            print(f"Attempting to get user: {username}")
            user = CustomUser.objects.get(username=username)
            print(f"Found user: {user}")
            is_approved = user.is_approved
            is_Wholesaler = user.is_Wholesaler
            is_OrdinaryCustomer = user.is_OrdinaryCustomer
        except CustomUser.DoesNotExist:
            print("User does not exist")
            raise forms.ValidationError('查無此帳號')
        
        if username is not None and password:
            print(f"Attempting to authenticate user: {username}")
            self.user_cache = authenticate(self.request, username=username, password=password, is_approved=is_approved, is_Wholesaler=is_Wholesaler, is_OrdinaryCustomer=is_OrdinaryCustomer)
            if self.user_cache is None:
                print("Authentication failed")
                raise self.get_invalid_login_error()
            else:
                print(f"Authenticated user: {self.user_cache}")
                self.confirm_login_allowed(self.user_cache)

        print("Cleaned data:", self.cleaned_data)
        return self.cleaned_data

    def get_user(self):
        return self.user_cache