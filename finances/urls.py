from django.urls import path
from .views import finances, ProductView, TransactionView

urlpatterns = [
    path('', finances, name='finances'),
    path('product/', ProductView.as_view(), name='product'),
    path('transaction/', TransactionView.as_view(), name='product_transaction'),

]
