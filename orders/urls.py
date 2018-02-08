# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


app_name = 'orders'

urlpatterns = [

	# url(r'^create/(?P<pk>\d+)/$', views.CreateOrderView.as_view(), name='OrderCreate'),
	# url(r'^create/$', views.create_order, name='OrderCreate'),
	url(r'^create/$', views.CreateOrderView.as_view(), name='OrderCreate'),

	url(r'^create/guest$', views.OrderCreateGuestView.as_view(), name='OrderCreateGuest'),
	
	url(r'^thanks-for-order/(?P<pk>\d+)/$', 
					views.ThanksForOrderView.as_view(), name='ThanksForOrder'),

	url(r'^pdf/(?P<pk>\d+)/$', views.GeneratePDF.as_view(), name= 'GeneratePDF'),

	# Чек-лист начала оформления заказа (купить без регистрации/зарегистрироваться/войти)
	# url(r'^check-order/$', views.CheckOrderView.as_view(), name='ChekOrder'),
	
]
