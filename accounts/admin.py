from django.contrib import admin
from.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', 'is_OrdinaryCustomer', 'is_Wholesaler', 'is_approved','is_staff')
    list_filter = ('is_OrdinaryCustomer', 'is_Wholesaler', 'is_approved')
    fieldsets = (
        (None, {'fields': ('username','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_approved', 'is_OrdinaryCustomer', 'is_Wholesaler','phone', 'address', 'email')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_OrdinaryCustomer', 'is_Wholesaler', 'is_approved','phone', 'address', 'email')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
