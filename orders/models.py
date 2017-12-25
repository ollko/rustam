# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.urls import reverse
from django.http import Http404

# Create your models here.
from accounts.models import GuestEmail

from shop.models import Product
from django.db.models.signals import post_save

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



def postal_code_validator(value):
	if value.isdigit and len(value)==6:
		return value
	raise ValidationError('Некоректный почтовый код')	

SHIPPINGCHOICES = (
	('с доставкой', 'Доставка в пределах Восточного Округа Москвы'), 
	('самовывоз', 'Самовывоз'), 
)
class Order(models.Model):
    
	guest_email = models.ForeignKey(GuestEmail,verbose_name = 'Email')
	session_key = models.CharField(verbose_name = 'Ключ текущей сессии', 
									max_length = 32, default='000', blank = True,)
	shipping 	= models.CharField(verbose_name = 'Выберите способ доставки:', max_length = 50, 
									choices = SHIPPINGCHOICES, default = 'с доставкой', )


	address 	= models.CharField(verbose_name='Адрес', max_length=250, 
									null = True, blank = True, default = None)
	postal_code = models.CharField(verbose_name='Почтовый код', max_length=20,
									validators = [postal_code_validator],
									null = True, blank = True, default = None,)
	city 		= models.CharField(verbose_name='Город', max_length=100, 
									null = True, blank = True, default = None,)
	created 	= models.DateTimeField(verbose_name='Создан', auto_now_add=True,)
	updated 	= models.DateTimeField(verbose_name='Обновлен', auto_now=True,)
	# paid = models.BooleanField(verbose_name='Оплачен', default=False)

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

		addr_to = instance.guest_email

		send_pdf_order(order_id, filename, addr_to)

		os.remove(filename)
		
		current_session.delete()


post_save.connect(post_save_receiver_order_model, sender=Order)



class Orderitem(models.Model):
	order = models.ForeignKey(Order, related_name='items')
	product = models.ForeignKey(Product, related_name='order_items')
	price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

	def __unicode__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity