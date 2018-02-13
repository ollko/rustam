# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Order, Orderitem

from django import forms
from django.db import models


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


SHIPPINGCHOICES = (
	('0', 'Доставка в пределах Восточного Округа Москвы'), 
	('1', 'Самовывоз'), 
)

class OrderAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderAdminForm, self).__init__(*args, **kwargs)
        self.fields['shipping'].widget = admin.widgets.AdminRadioSelect(choices = SHIPPINGCHOICES,)

class OrderAdmin(admin.ModelAdmin):

	form = OrderAdminForm

	list_display = ('user_email',
					'updated',
					OrderPDF,
					)

	fields =   ('user',
				'guest_profile',
				'shipping',
				# 'created',
				# 'updated',
				)
	readonly_fields = ('user','guest_profile',)
	list_filter = [ 'created', 'updated']
	inlines = [OrderItemInline]
	
	# formfield_overrides = {
	# 	models.CharField: {'widget': forms.RadioSelect},
	# }



admin.site.register(Order, OrderAdmin)


