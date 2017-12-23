# -*- coding: utf-8 -*-
from django import forms
from .models import GuestEmail



class GuestEmailForm(forms.ModelForm):
	class Meta:
		model = GuestEmail
		fields = ['email','guest_phone',]
		localized_fields = ('email','guest_phone',)

	def __init__(self, *args, **kwargs):
		super(GuestEmailForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget = forms.TextInput(attrs={
			'placeholder': u'123@yandex.ru',
			# 'id'		: ... ,
			# 'class'	: ... ,
			# 'name'	: ... ,
			})

		self.fields['guest_phone'].widget = forms.TextInput(attrs={
			'placeholder': u'+71234567890',			
			})

		
	def clean_email(self):
		email = self.cleaned_data.get("email")
		
		if email == "vasia@yandex.ru":
			raise forms.ValidationError("Введите корректный адрес.")
		return email
		
