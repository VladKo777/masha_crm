from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = ('name', 'provider', 'cost', 'currency',)
        fields = '__all__'

        def __str__(self):
            return self.name