# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView

from generic.mixins import CategoryListMixin

from shop.models import Product
from cart.forms import CartAddProductForm

from django.db.models import Q


class HomeView(CategoryListMixin, ListView):
	model = Product
	template_name = "home/home.html"
	queryset = Product.objects.all().order_by('-created')[:6]
	context_object_name = 'products'
	def get_context_data(self, **kwargs):
		context            				= super(HomeView, self).get_context_data(**kwargs)
		context['cart_product_form'] 	= CartAddProductForm()

		return context

class SearchView(CategoryListMixin, ListView):
	model = Product
	template_name = "home/search.html"
	# queryset = Product.objects.all().order_by('-created')[:6]
	context_object_name = 'products'
	def get_context_data(self, **kwargs):
		context            = super(SearchView, self).get_context_data(**kwargs)
		context['cart_product_form'] = CartAddProductForm()
		return context

	def get_queryset(self):
		qs = Product.objects.all()		
		query = self.request.GET.get('q')
		if query is not '':
			qs = qs.filter(Q(name__icontains=query) | Q(category__name__icontains=query)).distinct()
			return qs
		return




class AboutView(CategoryListMixin, TemplateView):
	template_name="home/about.html"


class ShippingView(CategoryListMixin, TemplateView):
	template_name="home/shipping.html"

class ContactsView(CategoryListMixin, TemplateView):
	template_name="home/contacts.html"


# from django.contrib.auth.views import LoginView

# class MyLoginView(LoginView):
# 	