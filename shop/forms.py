from django import forms
from .models import Product, Category

class ProductCreateForm(forms.ModelForm):
    """A form for creating new Products."""

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows':3, 'cols':20})}

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(id__in = [category.id for category in Category.objects.all() if category.is_leaf_node()])