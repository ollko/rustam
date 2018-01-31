# coding=utf-8
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [

	# url(r'^gestemail/$', views.CreateGestEmail.as_view(), name='CreateGestEmail'),
	url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile'),
	url(r'^createuser/$', views.CreateUserView.as_view(), name="createuser",),
	url(r'^confirm/$', views.ConfirmView.as_view(), name="confirm",),
	url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login",),
	url(r'^logout/$', auth_views.LogoutView.as_view(), name="logout",),
	url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'), 
]
