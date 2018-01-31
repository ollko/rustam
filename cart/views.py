# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import View, TemplateView

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


from generic.mixins import CategoryListMixin


@require_POST
def CartAdd(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data

		cart.add(product=product, quantity=cd['quantity'],
						update_quantity=cd['update'])
	return redirect('cart:CartDetail')

def CartRemove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:CartDetail')


class CartDetail(CategoryListMixin, TemplateView):

	template_name = 'cart/detail.html'

	def get_context_data(self, **kwargs):

		context = super(CartDetail, self).get_context_data(**kwargs)

		context['cart'] = Cart(self.request)
		for item in context['cart']:
			item['update_quantity_form'] = CartAddProductForm(
											initial={
											'quantity': item['quantity'],
											'update': True,
											})
		return context