from .api import api_urls
from django.urls import include, path
from .views import finances, ProductView, TransactionView

urlpatterns = [
    path('', finances, name='finances'),
    path('product/', ProductView.as_view(), name='product'),
    path('transaction/', TransactionView.as_view(), name='product_transaction'),
    path('api/', include(api_urls)),
]
