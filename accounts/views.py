# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your views here.
from django.views.generic import TemplateView, FormView, CreateView, UpdateView
from generic.mixins import CategoryListMixin
from django.contrib.auth import get_user_model, authenticate, login


from .models import GuestEmail, Profile
from .forms import GuestEmailForm, CurrentUserProfileForm
from accounts.forms import  UserCreationForm

class CreateGestEmail(CreateView):
	model 		= GuestEmail
	form_class 	= GuestEmailForm


User = get_user_model()


class ProfileView(CategoryListMixin, UpdateView):
	model = Profile	
	form_class = CurrentUserProfileForm
	template_name = 'accounts/profile.html'
	success_url = '/'


class CreateUserView(CategoryListMixin, FormView):

	template_name 	= 'accounts/createuser.html'
	form_class 		= UserCreationForm
	success_url 	= '/'

	def form_valid(self, form):

		email=form.cleaned_data['email']
		password=form.clean_password2()
		request=self.request

		user=User.objects.create_user(email,password)
		new_user = authenticate(request, email=email, password=password)
		login(request, user)
		return super(CreateUserView, self).form_valid(form)


class ConfirmView(TemplateView):
	template_name = 'accounts/confirm.html'


