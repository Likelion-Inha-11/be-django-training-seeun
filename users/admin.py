from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm
from .models import MyUser

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = MyUser
    list_display = ['email', 'nickname', 'mbti']    # 유저 목록에서 나타낼 정보
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nickname', 'mbti')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    filter_horizontal = []
    list_filter = ['is_active', 'is_admin'] # 필터링 옵션 - 추후
    ordering = ['email']    # 유저 정렬 기준

admin.site.register(MyUser, CustomUserAdmin)
