# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView

from .models import Order, Orderitem
from accounts.models import GuestEmail, Profile
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

from orders.forms import OrderCreateForm
from cart.views import CartDetail
from generic.mixins import CategoryListMixin

class GeneratePDF(View):
	def get(self, request, *args, **kwargs):
		template = get_template('other/invoice.html')
		current_order = get_object_or_404(Order, pk=kwargs['pk'])

		context = {
			# 'path_to_fonts':os.path.join(BASE_DIR,'static/fonts'),
			'path_to_fonts': BASE_DIR,
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


from django.core.exceptions import ObjectDoesNotExist

class CreateOrderView(CategoryListMixin, FormView):

	template_name 	= 'orders/order_form.html'
	form_class 		= OrderCreateForm
	success_url = '/'
	def get_initial(self):

		"""
		Returns the initial data to use for forms on this view.
		"""
		initial = super(CreateOrderView, self).get_initial()
		
		user 	= self.request.user
		initial['user'] 		= user
		
		try:
			p = user.profile
		except ObjectDoesNotExist:
			pass
		else:
			
			initial['full_name']	= p.full_name
			initial['phone']	 	= p.phone
			initial['address']		= p.address
		finally:
			return initial

		
	def form_invalid(self, form):
		return super(CreateOrderView, self).form_invalid(form)

	def form_valid(self, form):
		"""
		If the form is valid, redirect to the supplied URL.
		"""
		user 	= self.request.user
	
		try:
			p = user.profile
		except ObjectDoesNotExist:
			p = Profile(user=user)
			p.save()

		p.full_name 	= form.cleaned_data['full_name']
		p.phone 		= form.cleaned_data['phone']
		p.address 		= form.cleaned_data['address']

		p.save()

		o 	= Order(user=user,
					session_key=self.request.session.session_key,
					shipping = form.cleaned_data['shipping'])
		o.save()
		return super(CreateOrderView, self).form_valid(form)


	def get_success_url(self):
		# Clear cart after order create
		
		cart=Cart(self.request)
		cart.clear()

		return super(CreateOrderView, self).get_success_url()


class ThanksForOrderView(TemplateView):
	template_name = 'orders/thanks_for_order.html'

	def get_context_data(self, **kwargs):
		context = super(ThanksForOrderView, self).get_context_data(**kwargs)
		context['order_id']    = kwargs['pk']
		current_order = get_object_or_404(Order, pk=kwargs['pk'])
		context['user_email'] = current_order.user
		return context
			

