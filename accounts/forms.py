# -*- coding: utf-8 -*-
from django import forms
from .models import GuestEmail, Profile

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

User = get_user_model()

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
		


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user





class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class CurrentUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = ('full_name','phone','address','postal_code','city',)
        fields = ('user','full_name','phone','address',)


    def __init__(self, *args, **kwargs):
        super(CurrentUserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            self.fields['user'].required = False
            self.fields['user'].widget.attrs['disabled'] = 'disabled'

    def clean_user(self):
        
        instance = getattr(self, 'instance', None)
        if instance :

            return instance.user
        else:
            return self.cleaned_data.get('user', None)


class UserCreationForm(UserAdminCreationForm):
    """Includes fields:
    'email'
    """
    consent = forms.BooleanField(required=True)



