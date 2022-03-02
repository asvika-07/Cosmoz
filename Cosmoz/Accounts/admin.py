from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Accounts.models import User

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "RegistrationID",
        "date_joined",
        "last_login",
        "is_admin",
        "is_staff",
    )
    search_fields = ("email", "username", "RegistrationID")
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, AccountAdmin)
