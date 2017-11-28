from django.conf.urls import url
from . import views


app_name = 'home'

urlpatterns = [

	url(r'^$', views.HomeView.as_view(), name="home",),

	url(r'^about/$', views.AboutView.as_view(), name="about",),

	url(r'^shipping/$', views.ShippingView.as_view(), name="shipping",),

	url(r'^contacts/$', views.ContactsView.as_view(), name="contacts",),

]