# coding=utf-8
from django.conf.urls import url
from . import views


app_name = 'backapp'

urlpatterns = [

	url(r'^orderlist/$', views.OrderListView.as_view(), name='orderlist',),

	url(r'^edit/$', views.EditView.as_view(), name='edit',),

	url(r'^(?P<category_slug>[-\w]+)/product-list-with-edit/$',
				views.ProductListEditView.as_view(), 
		    	name='product_list_by_category_with_edit',),


	url(r'^create/$', views.ProductCreateView.as_view(), name='product_create',),

	url(r'^(?P<pk>\d+)/update/$', views.ProductUpdate.as_view(), 
						    	name='product_update',),

	url(r'^(?P<pk>\d+)/delete/$', views.ProductDelete.as_view(), 
								name='product_delete',),

	url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/success/$', views.ProductSuccessDetail.as_view(), name='product_detail_success',),
	
]
