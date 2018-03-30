from django import forms
from .models import Product

class ProductCreateForm(forms.ModelForm):
    """A form for creating new Products."""

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows':3, 'cols':20})}
