# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.urls import reverse
# Create your models here.

from phonenumber_field.modelfields import PhoneNumberField

class GuestEmail(models.Model):

	email        = models.EmailField(verbose_name='Ваш email:',)
	guest_phone  = PhoneNumberField(verbose_name='Ваш телефон:', default=None, null=True)
	active       = models.BooleanField(default=True)
	update       = models.DateTimeField(auto_now=True)
	timestamp    = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Гостевой email'
		verbose_name_plural = 'Гостевые emails'

	def __unicode__(self):
		return self.email

	def get_absolute_url(self):
		return reverse('orders:OrderCreate', kwargs={'pk': self.pk})

	