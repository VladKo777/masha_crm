from django.urls import path
from .views import finances, ProductView

urlpatterns = [
    path('', finances, name='finances'),
    path('product/', ProductView.as_view(), name='product'),

]