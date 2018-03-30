# coding=utf-8
from django.conf.urls import url
from . import views


app_name = 'shop'

urlpatterns = [

	


	url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList.as_view(), name='product_list_by_category'),

	

	url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail.as_view(), name='product_detail',),
]
