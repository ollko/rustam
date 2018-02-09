# -*- coding: utf-8 -*-
from django import forms
from .models import Order



# class OrderCreateForm(forms.ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = ['shipping','address','postal_code','city']
# 		widgets = {
# 			'shipping'	: forms.RadioSelect,
# 			# 'address'	: forms.TextInput(placeholder = 'Москва, Кусковская, 12',),	
# 		}
# 	def __init__(self, *args, **kwargs):
# 		super(OrderCreateForm, self).__init__(*args, **kwargs)
# 		# self.fields['address'].widget = forms.TextInput(attrs={
# 		# 	'placeholder': u'Кусковская 12',
# 		# 	# 'id'		: ... ,
# 		# 	# 'class'	: ... ,
# 		# 	# 'name'	: ... ,
# 		# 	})

# 		# self.fields['postal_code'].widget = forms.TextInput(attrs={
# 		# 	'placeholder': u'123456',			
# 		# 	})

# 		# self.fields['city'].widget = forms.TextInput(attrs={
# 		# 	'placeholder': u'Москва',			
# 		# 	})
# 		pass

# 	def clean_address(self):
# 		shipping = self.cleaned_data.get("shipping")
# 		address = self.cleaned_data.get("address")
# 		if shipping==u'с доставкой' and address==None :
			
# 			raise forms.ValidationError("Введите адрес!")
# 		return address

# 	def clean_postal_code(self):
# 		shipping = self.cleaned_data.get("shipping")
# 		postal_code = self.cleaned_data.get("postal_code")
		
# 		if shipping==u'с доставкой' and postal_code==None :
# 			raise forms.ValidationError("Введите почтовый код!")
# 		return postal_code

# 	def clean_city(self):
# 		shipping = self.cleaned_data.get("shipping")
# 		city = self.cleaned_data.get("city")
		
# 		if shipping==u'с доставкой' and city==None :
# 			raise forms.ValidationError("Введите город!")
# 		return city

from accounts.forms import CurrentUserProfileForm, GuestUserProfileForm
from .models import SHIPPINGCHOICES


class OrderCreateForm(CurrentUserProfileForm):
	"""Includes fields:
	
	'full_name',
	'phone',
	'address',
	'shipping'
	"""
	shipping = forms.ChoiceField(label='',required = True, widget=forms.RadioSelect, 
				choices=SHIPPINGCHOICES, initial=('0', 'Доставка в пределах Восточного Округа Москвы'))
	
	# def __init__(self, *args, **kwargs):
	# 	super(OrderCreateForm, self).__init__(*args, **kwargs)
		# self.fields['user'].required = False
		# self.fields['user'].widget.attrs['disabled'] = 'disabled'


	def clean_user(self):		
		pass
		

	def clean(self):
		cleaned_data =super(OrderCreateForm, self).clean()
		shipping = self.cleaned_data.get("shipping")
		address = self.cleaned_data.get("address")

		if shipping==u'0' and address==None :
			msg ="Введите адрес доставки!"
			self.add_error('address', msg)
            
	

class OrderForGestCreateForm(GuestUserProfileForm):
	"""Includes fields:
	'user'  (uneditable field),
	'full_name',
	'phone',
	'address',
	'shipping'
	"""

	shipping = forms.ChoiceField(label='',required = True, widget=forms.RadioSelect, 
				choices=SHIPPINGCHOICES, initial=('0', 'Доставка в пределах Восточного Округа Москвы'))
	
	def clean(self):
		cleaned_data =super(OrderForGestCreateForm, self).clean()
		shipping = self.cleaned_data.get("shipping")
		address = self.cleaned_data.get("address")

		if shipping==u'0' and address==None :
			msg ="Введите адрес доставки!"
			self.add_error('address', msg)