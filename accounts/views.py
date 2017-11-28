# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView
from accounts.models import GuestEmail

class CreateGestEmail(CreateView):
	model = GuestEmail
	fields = ['email']