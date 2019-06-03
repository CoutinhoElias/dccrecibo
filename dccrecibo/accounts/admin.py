from django.contrib import admin

# Register your models here.
from dccrecibo.accounts.models import UserAdress


@admin.register(UserAdress)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    # search_fields = ('cdalterdata', 'name', 'email')
