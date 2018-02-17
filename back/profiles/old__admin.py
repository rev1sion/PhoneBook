from django.contrib import admin
from back.profiles.models import Position, UserGroup, User, Avatar


class UserGroupInline(admin.TabularInline):
    model = UserGroup
    extra = 0


# class PositionInline(admin.TabularInline):
#     model = Position
#     extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserGroupInline]


class UserInline(admin.TabularInline):
    extra = 0
    model = User
# @admin.register(User)
# class UserGroupAdmin(admin.ModelAdmin):
#     list_display = )


admin.site.register(UserGroup),
admin.site.register(Avatar),
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    inlines = [UserInline]