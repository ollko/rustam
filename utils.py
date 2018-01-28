# -*- coding: utf-8 -*-


def postal_code_validator(value):
	if value.isdigit and len(value)==6:
		return value
	raise ValidationError('Некоректный почтовый код')	
