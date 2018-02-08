# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from .models import Profile, GuestProfile

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm

from django.contrib.auth import get_user_model
User = get_user_model()


class ProfileItemInline(admin.TabularInline):
    model = Profile
    raw_id_field = ['full_name',
                    'phone',
                    'address',
                    'postal_code',
                    'city',
                    ]

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin','id',)
    list_filter = ('admin','staff','active')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin','staff','active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    inlines = [ProfileItemInline]

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


admin.site.register(User, UserAdmin)


admin.site.register(Profile)


admin.site.register(GuestProfile)
