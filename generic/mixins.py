# coding=utf-8
from django.views.generic.base import ContextMixin
from shop.models import Category


class CategoryListMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(CategoryListMixin, self).get_context_data(**kwargs)
		context["nodes"]		= Category.objects.all()
		context['current_url']  = self.request.path
		context['user']			= self.request.user
		# print "context['user']", context['user'].first_name
		return context