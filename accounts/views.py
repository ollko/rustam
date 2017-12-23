# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView
from .models import GuestEmail
from .forms import GuestEmailForm


class CreateGestEmail(CreateView):
	model 		= GuestEmail
	form_class 	= GuestEmailForm
	