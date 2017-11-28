from django import forms
from django.contrib.admin.widgets import AdminIntegerFieldWidget

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
	# quantity = forms.IntegerField(initial=1, widget=forms.HiddenInput)
	quantity = forms.TypedChoiceField(label='',choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)