# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView

from generic.mixins import CategoryListMixin

from shop.models import Product
from cart.forms import CartAddProductForm

# Create your views here.
class HomeView(ListView, CategoryListMixin):
	model = Product
	template_name = "home/home.html"
	queryset = Product.objects.all().order_by('-created')[:6]
	context_object_name = 'products'
	def get_context_data(self, **kwargs):
		context            = super(HomeView, self).get_context_data(**kwargs)
		context['cart_product_form'] = CartAddProductForm()

		return context

class AboutView(TemplateView, CategoryListMixin):
	template_name="home/about.html"


class ShippingView(TemplateView, CategoryListMixin):
	template_name="home/shipping.html"

class ContactsView(TemplateView, CategoryListMixin):
	template_name="home/contacts.html"