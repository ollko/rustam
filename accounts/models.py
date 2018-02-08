# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField



from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
)

from utils import postal_code_validator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,

        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
	email 			= models.EmailField(verbose_name = "Эл. почта:", max_length=255, unique=True)

	active 			= models.BooleanField(default=True) # can login
	staff			= models.BooleanField(default=False) # staff user non super
	admin			= models.BooleanField(default=False) # superuser
	is_active 		= models.BooleanField(default=True)
	timestamp		= models.DateTimeField(auto_now_add=True)
	# confirm 		= models.BooleanField(default=False)
	# confirmed_date	= models.DateTimeField(default=False)

	USERNAME_FIELD = 'email' # username
	# USERNAME_FIELD and password are required by default
	REQUIRED_FIELDS = [] #['full_name'] # python manage.py createsuperuser


	objects = UserManager()


	def __unicode__(self):
		return self.email

	# def get_full_name(self):
	# 	return self.email
	
	def get_short_name(self):
		return self.email


	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		return self.staff
	
	@property
	def is_admin(self):
		return self.admin

	# @property
	# def is_active(self):
	# 	return self.active

class Profile(models.Model):
	user 			= models.OneToOneField(User,verbose_name='Логин:', on_delete = models.CASCADE)
	full_name		= models.CharField(verbose_name='Полное имя:', max_length=255,)
	phone 			= PhoneNumberField(verbose_name='Tелефон:',)
	address 		= models.CharField(verbose_name='Адрес:',
										max_length=250,
										null=True,
										blank=True,
										default=None,
										)
	postal_code 	= models.CharField(verbose_name='Почтовый код:', max_length=20,
									validators = [postal_code_validator],
									null = True, blank = True, default = None,)
	city 			= models.CharField(verbose_name='Город:', max_length=100, 
									null = True, blank = True, default = None,)
	# extend extra data


# class GuestEmail(models.Model):

# 	email        = models.EmailField(verbose_name='Ваш email:',)
# 	update       = models.DateTimeField(auto_now=True)
# 	timestamp    = models.DateTimeField(auto_now_add=True)

# 	class Meta:
# 		verbose_name = 'Гостевой email'
# 		verbose_name_plural = 'Гостевые emails'

# 	def __unicode__(self):
# 		return self.email

	# def get_absolute_url(self):
	# 	return reverse('orders:OrderCreate', kwargs={'pk': self.pk})


class GuestProfile(models.Model):
	user 			= models.EmailField(verbose_name='Ваш email:',)
	full_name		= models.CharField(verbose_name='Полное имя:', max_length=255,)
	phone 			= PhoneNumberField(verbose_name='Tелефон:',)
	address 		= models.CharField(verbose_name='Адрес:',
										max_length=250,
										null=True,
										blank=True,
										default=None,
										)
	postal_code 	= models.CharField(verbose_name='Почтовый код:', max_length=20,
									validators = [postal_code_validator],
									null = True, blank = True, default = None,)
	city 			= models.CharField(verbose_name='Город:', max_length=100, 
									null = True, blank = True, default = None,)

	def __unicode__(self):
		return self.user