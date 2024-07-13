from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def user_is_Wholesaler(user):
    return user.is_Wholesaler  # 或任何檢查管理員角色的條件

def Wholesaler_required(view_func):
    decorated_view_func = user_passes_test(user_is_Wholesaler, login_url='/login/')
    return decorated_view_func(view_func)
