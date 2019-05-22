from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Goal, DietData, Activity
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'], code='duplicate_username')


class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('dob', 'gender',
                                                          'heightUnits', 'weightUnits', 'height', 'weight',
                                                          'exerciseIntensity')}),)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Goal)
admin.site.register(DietData)
admin.site.register(Activity)
