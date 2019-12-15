from django import forms
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = ('name', 'provider', 'cost', 'currency',)
        fields = '__all__'

        def __str__(self):
            return self.name


class TransactionForm(forms.ModelForm):
    rate = forms.DecimalField(max_digits=12, decimal_places=6, label=('вартість'))

    class Meta:
        model = Transaction
        fields = ('sent_to', 'product', 'value', 'surcharge', 'rate')

        def __str__(self):
            return self.name

    class Meta:
        model = Transaction
        fields = ('sent_to', 'product', 'value', 'surcharge', 'rate')
        labels = {
            'sent_to': 'Клієнт',
            'product': "Продукт",
            'value': "Вартість",
            'surcharge': "Націнка",

        }