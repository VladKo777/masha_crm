from django.urls import include, path
from .views import finances, ProductView, TransactionView

urlpatterns = [
    path('', finances, name='finances'),
    path('api/', include('finances.api.urls')),
    path('product/', ProductView.as_view(), name='product'),
    path('transaction/', TransactionView.as_view(), name='product_transaction'),

]
