from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin

customUser = settings.AUTH_USER_MODEL


class CustomUserAdmin(UserAdmin):
    model = customUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('dob', 'gender',
                                                          'heightUnits', 'weightUnits', 'height', 'weight',)}))


admin.register(customUser, CustomUserAdmin)
