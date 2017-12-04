# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from .models import Order, Orderitem
from accounts.models import GuestEmail
from cart.cart import Cart

from django.http import HttpResponse


from django.views.generic import View
from django.template.loader import get_template

from.utils import render_to_pdf

import os
from django.shortcuts import get_object_or_404

from decimal import Decimal


from rustam2.settings.production import BASE_DIR

try:
	from rustam2.settings.local import BASE_DIR
except:
	pass

class GeneratePDF(View):
	def get(self, request, *args, **kwargs):
		template = get_template('other/invoice.html')
		current_order = get_object_or_404(Order, pk=kwargs['pk'])

		context = {
			'path_to_fonts':os.path.join(BASE_DIR,'static/fonts'),
			'order': current_order,
		}
		
		html = template.render(context)
		pdf = render_to_pdf('other/invoice.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Заказ_%s.pdf" %(current_order.id)
			content = "inline; filename='%s'" %(filename)

			# for downloading
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse('Not found')


class CreateOrderView(CreateView):
	model = Order
	fields = ['address','postal_code','city']

	def form_valid(self, form):
		"""
		If the form is valid, save the associated model.
		"""
		
		form.instance.guest_email = GuestEmail.objects.get(pk=self.kwargs['pk'])
		form.instance.session_key = self.request.session.session_key
		return super(CreateOrderView, self).form_valid(form)

	
class ThanksForOrderView(TemplateView):
	template_name = 'orders/thanks_for_order.html'

	def get_context_data(self, **kwargs):
		context = super(ThanksForOrderView, self).get_context_data(**kwargs)
		context['order_id']    = kwargs['pk']
		current_order = get_object_or_404(Order, pk=kwargs['pk'])
		context['guest_email'] = current_order.guest_email.email
		return context
			