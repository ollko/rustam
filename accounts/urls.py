# coding=utf-8
from django.conf.urls import url
from . import views


app_name = 'accounts'

urlpatterns = [

	url(r'^gestemail/$', views.CreateGestEmail.as_view(), name='CreateGestEmail'),

]
