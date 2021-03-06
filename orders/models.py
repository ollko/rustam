# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.urls import reverse
from django.http import Http404

# Create your models here.
from accounts.models import GuestProfile

from shop.models import Product
from django.db.models.signals import pre_save, post_save

from django.contrib.sessions.models import Session
# from django.contrib.sessions.backends.db import SessionStore

from django.conf import settings
from django.core.exceptions import ValidationError
import os

from rustam2.settings.production import BASE_DIR

try:
	from rustam2.settings.local import BASE_DIR
except:
	pass

from.utils import write_pdf_to_disk, send_pdf_order

from django.forms import RadioSelect

from django.contrib.auth import get_user_model
User = get_user_model()

def postal_code_validator(value):
	if value.isdigit and len(value)==6:
		return value
	raise ValidationError('Некоректный почтовый код')	

SHIPPINGCHOICES = (
	('0', 'Доставка в пределах Восточного Округа Москвы'), 
	('1', 'Самовывоз'), 
)
class Order(models.Model):
    
	user 			= models.ForeignKey(User,
										verbose_name = 'Авторизованный клиент', 
										default = None,
										null = True,
										on_delete = models.CASCADE,
										)
	guest_profile   = models.ForeignKey(GuestProfile,
										verbose_name = 'Гость',
										default = None,
										null = True,
										on_delete = models.CASCADE,
										)
	session_key		= models.CharField(verbose_name = 'Ключ текущей сессии', 
										max_length = 32,
										default='000',
										blank = True,
										)
	shipping 		= models.CharField(verbose_name = 'Выберите способ доставки:',
										max_length = 1,
										choices = SHIPPINGCHOICES,
										default = '0',
										)

	created 		= models.DateTimeField(verbose_name='Создан',
										auto_now_add=True,
										)
	updated 		= models.DateTimeField(verbose_name='Обновлен',
										auto_now=True,
										)



	class Meta:
		ordering 			= ('-created', )
		verbose_name 		= 'Заказ'
		verbose_name_plural = 'Заказы'

		# widgets 	= 	{
		# 			'shipping': RadioSelect,
		# 			}

	def __unicode__(self):
		return 'Заказ: {}'.format(self.id)

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

	def get_absolute_url(self):
		return reverse('orders:ThanksForOrder', kwargs={'pk': self.pk})

	@property
	def shipping_boolean(self):
		if self.shipping=='0':
			return True
		return False

	@property
	def shipping_status(self):
		if self.shipping=='0':
			return 'С доставкой'
		return 'Самовывоз'	

	# @property
	# def user_status(self):
	# 	if self.user:
	# 		return 'С регистрацией'
	# 	if self.guest_profile:
	# 		return 'Без регистрации'


	def user_status_property(self):
		if self.user:
			return 'С регистрацией'
		if self.guest_profile:
			return 'Без регистрации'
	user_status_property.short_description = 'Статус клиента'	

	user_status = property(user_status_property)


	# @property
	# def user_email(self):
	# 	if self.user:
	# 		return self.user.email
	# 	if self.guest_profile:
	# 		return self.guest_profile.user

	def user_email_property(self):
		if self.user:
			return self.user.email
		if self.guest_profile:
			return self.guest_profile.user
	user_email_property.short_description = 'Электронная почта'	

	user_email = property(user_email_property)



def post_save_receiver_order_model(sender, instance, created, **kwargs):

	if created:
		session_key = instance.session_key
		order = instance
		try:
			current_session = Session.objects.get(pk=session_key)
		except Session.DoesNotExist:
			raise Http404("Текущая сессия не сохранилась:(")
		# get cat from  session:
		cart = current_session.get_decoded()['cart']
		# save item from cart to created order:
		for key, value in cart.items():
			product = Product.objects.get(pk=key)
			
			Orderitem.objects.create(order = order, product = product,
									price=value['price'],
									quantity=value['quantity'])
		
		# writing pdf to disk:
		order_id = instance.id
		filename = os.path.join(BASE_DIR,"orders/tmp/Order_%s.pdf")%(order_id)

		context = {
				'path_to_fonts':os.path.join(BASE_DIR,'static/fonts'),
				'order': instance,
			}
		write_pdf_to_disk('other/invoice.html', filename, context)

		addr_to = instance.user

		send_pdf_order(order_id, filename, addr_to)

		os.remove(filename)
		
		

post_save.connect(post_save_receiver_order_model, sender=Order)



class Orderitem(models.Model):
	order = models.ForeignKey(Order, related_name='items',on_delete = models.CASCADE)
	product = models.ForeignKey(Product, verbose_name='Позиция заказа', related_name='order_items')
	price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

	def __unicode__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity