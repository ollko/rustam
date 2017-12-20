# coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter
# Register your models here.
from .models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'name', 'category')
    list_filter = (('category', TreeRelatedFieldListFilter),)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        kwargs["queryset"] = Category.objects.filter(id__in=[category.id for category in Category.objects.all() if category.is_leaf_node()])

        return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Product,ProductAdmin)

# admin.site.register(Category, MPTTModelAdmin)

# class CustomMPTTModelAdmin(MPTTModelAdmin):
	# specify pixel amount for this ModelAdmin only:
	# mptt_level_indent = 20

# admin.site.register(Category, CustomMPTTModelAdmin)

admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'id',
        'lft',
        'tree_id',
        'rght',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)