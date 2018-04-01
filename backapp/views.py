# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy

from orders.models import Order
from shop.models import Product, Category
from generic.mixins import CategoryListMixin
from shop.forms import ProductCreateForm

# Create your views here.
class OrderListView(PermissionRequiredMixin, CategoryListMixin, ListView):
	permission_required = 'product.can_add'
	model = Order
	context_object_name = 'orders'
	template_name = 'backapp/order_list.html'
	paginate_by = 10
	paginate_orphans = 1

	# def get_qweryset

class EditView(PermissionRequiredMixin, CategoryListMixin, TemplateView):
	permission_required = 'product.can_add'
	template_name = 'backapp/edit_view.html'

class ProductCreateView(PermissionRequiredMixin, CategoryListMixin, CreateView):
	permission_required = 'product.can_add'
	model = Product
	context_object_name = 'product'
	form_class = ProductCreateForm

	def get_success_url(self):
		self.success_url = self.object.get_after_create_url()
		return super(ProductCreateView, self).get_success_url()

# На этой странице список товара для редактирования:
class ProductListEditView(PermissionRequiredMixin, CategoryListMixin, ListView):
	permission_required = 'product.can_add'
	model = Product
	context_object_name = 'products'
	template_name = 'backapp/product_edit_list.html'


	def get_queryset(self):
		'''список продуктов для меню с двумя уровнями влоденности
		(каталог/подкаталог/продукт)'''
		if 'category_slug' in self.kwargs:
			current_cat = get_object_or_404(Category, slug= self.kwargs['category_slug'])
			if current_cat.is_leaf_node():

				return Product.objects.filter(category__slug = self.kwargs['category_slug'])
			else:
				res=[] 
				for cat in current_cat.get_descendants():
					res+=Product.objects.filter(category__slug = cat.slug)
				return res
		else:
			return Product.objects.all()


	def get_context_data(self, **kwargs):
		context = super(ProductListEditView, self).get_context_data(**kwargs)
		
		if 'category_slug' in self.kwargs:
			
			context['category'] = Category.objects.get(slug = self.kwargs['category_slug'])

		return context

class ProductUpdate(PermissionRequiredMixin, CategoryListMixin, UpdateView):
	permission_required = 'product.can_change'
	model = Product
	fields = '__all__'


	def get_context_data(self, **kwargs):
		context = super(ProductUpdate, self).get_context_data(**kwargs)
		current_product = Product.objects.get(pk = self.kwargs['pk'])
		context['back_url'] = '/backapp/'+ current_product.category.slug+'/product-list-with-edit/'
		return context


class ProductDelete(PermissionRequiredMixin, CategoryListMixin, DeleteView):
	permission_required = 'product.can_delete'
	model = Product
	success_url = '/'
	success_url = reverse_lazy('backapp:edit')

	def get_context_data(self, **kwargs):
		context = super(ProductDelete, self).get_context_data(**kwargs)
		current_product = Product.objects.get(pk = self.kwargs['pk'])
		context['back_url'] = '/backapp/'+ current_product.category.slug+'/product-list-with-edit/'
		return context

	def get_success_url(self):
		self.success_url = 	'/backapp/' + Product.objects.get(pk = self.kwargs['pk']).category.slug + '/product-list-with-edit/'
		return super(ProductDelete, self).get_success_url()



class ProductSuccessDetail(PermissionRequiredMixin, CategoryListMixin, DetailView):
	permission_required = 'product.can_add'
	model = Product
	context_object_name = 'product'
	template_name = 'backapp/product_detail_edit.html'

	def get_context_data(self, **kwargs):
		context = super(ProductSuccessDetail, self).get_context_data(**kwargs)
		context['category'] = Category.objects.get(cat=self.kwargs['pk'])
		# Вместо 'cat' может быть - cat, children, id, level, lft, name, parent, parent_id, rght, slug, tree_id
		return context 

	def get_object(self, queryset=None):
		'''
		Проверяется правильный ли slug для страницы товара, 
		а затем возвращает obj
		'''
		obj = super(ProductSuccessDetail, self).get_object(queryset=queryset)
		if obj.slug != self.kwargs['slug']:
			raise Http404("Страница не найдена")
		return obj