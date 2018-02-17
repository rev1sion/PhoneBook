from django.contrib import admin
from back.companies.models import Office, Organization
from back.profiles.models import User

# admin.site.register(Organization)
# class OrganizationInline(admin.TabularInline):
#     model = Organization
#     extra = 0
#
#
# @admin.register(Office)
# class OfficeAdmin(admin.ModelAdmin):
#     inlines = [OrganizationInline]


# class UserInline(admin.TabularInline):
#     model = User
#     extra = 0


class OfficeInline(admin.TabularInline):
    model = Office
    extra = 0


@admin.register(Organization)
class OrgAdmin(admin.ModelAdmin):
    inlines = [OfficeInline]


admin.site.register(Office)
# @admin.register(Office)
# class OfficeAdmin(admin.ModelAdmin):
#     inlines = [UserInline]