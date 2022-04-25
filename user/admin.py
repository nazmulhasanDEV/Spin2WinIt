from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import *

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'username', 'phone_no',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'password', 'username', 'phone_no', 'is_active', 'is_admin', 'is_seller', 'is_buyer', 'is_a_staff',)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'phone_no', 'is_admin', 'is_seller', 'is_buyer', 'is_a_staff')
    list_filter = ('is_admin', 'is_seller', 'is_buyer', 'is_a_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phone_no', 'fname', 'lname', 'nid_no', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin', 'is_seller', 'is_buyer', 'is_a_staff', 'is_active', 'status')}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_no', 'nid_no', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Account, UserAdmin)
admin.site.unregister(Group)


admin.site.register(UserProfilePicture)
admin.site.register(ResetPermissionStatus)
admin.site.register(VerificationCode)

admin.site.register(BillingInfo)
admin.site.register(ShippingInfo)

# disclaimer ip list
admin.site.register(DisclaimerAgreeDisagreeIPList)