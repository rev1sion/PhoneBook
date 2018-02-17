from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from back.profiles.models import User, PhoneNumber
from back.companies.admin import OfficeInline


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Повторите пароль'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'full_name',
            'bio',
            'email',
            'avatar',
            'position',
            'is_active',
            'birthday',
            'accepted_tos',
            'is_admin'
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Пароли не совпадают"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'birthday',
            'avatar',
            'position',
            'full_name',
            'bio',
            'accepted_tos', 'is_active', 'is_admin',
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_city', 'phone_mobile', 'phone_small',)
    list_filter = ('phone_small', 'phone_city', 'phone_mobile',)
    search_fields = ('phone_city', 'phone_mobile', 'phone_small',)


class PhoneNumberInlineAdmin(admin.TabularInline):
    # inlines = [UserInlineAdmin,]
    model = PhoneNumber
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = [PhoneNumberInlineAdmin ]
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'full_name',
        'is_admin',
        'position',
    )
    list_filter = ('position', 'full_name',)
    fieldsets = (
        (_('Персональная информация'), {'fields': (
            'full_name',
            'birthday',
            'position',
            'avatar',
            'bio',
        )}),
        (None, {'fields': ('email', 'password',)}),
        (_('Права'), {'fields': (('is_admin', 'accepted_tos', 'is_active'),)}),
        (_('Создан'), {'fields': (('created_at', 'updated_at'),)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                # 'uuid',
                'email',
                'full_name',
                'position',
                'bio',
                'avatar',
                ('birthday',
                'accepted_tos','is_active', 'is_admin'),
                ('password1',
                'password2'),
                # ('created_at', 'updated_at')
            )}
         ),
    )
    readonly_fields = ('uuid', 'created_at', 'updated_at',)
    search_fields = ('full_name', 'email', 'position')
    ordering = ('full_name',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


