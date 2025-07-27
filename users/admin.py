from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import userRegistration
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('phone_number',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    search_fields = UserAdmin.search_fields + ('phone_number',)

admin.site.register(userRegistration, CustomUserAdmin)    

