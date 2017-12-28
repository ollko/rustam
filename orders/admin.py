# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Order, Orderitem


class OrderItemInline(admin.TabularInline):
	model = Orderitem
	raw_id_field = ['product',
					'price',
					'quantity',]


from django.utils.html import format_html
from django.core.urlresolvers import reverse

def OrderPDF(obj):
	return format_html('<a href="{}">PDF</a>'.format(
		reverse('orders:GeneratePDF', args=[obj.id])
	))
OrderPDF.short_description = 'В PDF'					



class OrderAdmin(admin.ModelAdmin):
	list_display = ('guest_email',
					'address',
					'postal_code',
					'city',
					'created',
					OrderPDF,
					)

	fields =   ('guest_email',
				'address',
				'postal_code',
				'city',
				'shipping',
				'shipping_state'
				)
	# list_filter = [ 'created', 'updated']
	inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

