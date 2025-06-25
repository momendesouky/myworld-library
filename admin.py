from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, BorrowRecord, User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_admin')
    fieldsets = UserAdmin.fieldsets + (
        ('Library Admin', {'fields': ('is_admin',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Book)
admin.site.register(BorrowRecord)