# coding=utf-8
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse
from django.template import loader, Context, RequestContext

from .models import Category, Product

from generic.mixins import CategoryListMixin

from cart.forms import CartAddProductForm

from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin


# def show_tree(request):
	
# 	return render(request,"shop/tree.html",{'nodes':Category.objects.all()})

# Страница товаро из категории:
class ProductList(ListView, CategoryListMixin):

	model = Product
	context_object_name = 'products'
	template_name = 'shop/product_list.html'
	paginate_by = 6
	paginate_orphans = 1

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
		context = super(ProductList, self).get_context_data(**kwargs)
		
		if 'category_slug' in self.kwargs:
			
			context['category'] = Category.objects.get(slug = self.kwargs['category_slug'])

		context['cart_product_form'] = CartAddProductForm()
		return context

# Страница товара
class ProductDetail(DetailView, CategoryListMixin):
	model = Product
	context_object_name = 'product'
	template_name = 'shop/product_detail.html'
	def get_context_data(self, **kwargs):
		context = super(ProductDetail, self).get_context_data(**kwargs)
		context['category'] = Category.objects.get(cat=self.kwargs['pk'])
		print 'context["category"]=', context['category'].__dict__
		# Вместо 'cat' может быть - cat, children, id, level, lft, name, parent, parent_id, rght, slug, tree_id
		context['cart_product_form'] = CartAddProductForm()

		return context 

	def get_object(self, queryset=None):
		'''
		Проверяется правильный ли slug для страницы товара, 
		а затем возвращает obj
		'''
		obj = super(ProductDetail, self).get_object(queryset=queryset)
		if obj.slug != self.kwargs['slug']:
			raise Http404("Страница не найдена")
		return obj


class ProductCreate(PermissionRequiredMixin, CreateView, CategoryListMixin):
	permission_required = 'product.can_add'
	model = Product
	fields = '__all__'
	context_object_name = 'product'	
	

class ProductUpdate(PermissionRequiredMixin, UpdateView, CategoryListMixin):
	permission_required = 'product.can_change'
	model = Product
	fields = '__all__'
	

class ProductDelete(PermissionRequiredMixin, DeleteView, CategoryListMixin):
	permission_required = 'product.can_delete'
	model = Product
	success_url = '/'
	# success_url = reverse_lazy('main:main_page')
	# def get_context_data(self, **kwargs):
	# 	context = super(ServiceDelete, self).get_context_data(**kwargs)
	# 	context['back_url'] = '/services/'+ self.kwargs['pk']
	# 	print "context['back_url']=",context
	# 	return context
# 