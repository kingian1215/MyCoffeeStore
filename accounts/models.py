from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
# Create your models here.

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=True) 
    # 有效用户 預設為 False,若不想人工審核,可直接設為 True
    is_OrdinaryCustomer = models.BooleanField(default=False) # 用戶別為普通顧客
    is_Wholesaler = models.BooleanField(default=False) # 用戶別為批發商
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self): #用戶名
        return self.username

    class Meta:
        permissions = [
            ("can_view", "可查看模型"),
            ("can_edit", "可編輯模型"),
        ]
