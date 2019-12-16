from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Account
from .forms import ProductForm, TransactionForm
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView
from .api.serializers import TransactionSerializer


# @add_ability_to_create_many_objects
class CreateTransactionAPIView(CreateAPIView):
    serializer_class = TransactionSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@login_required
def finances(request):
    return render(request, "finances.html")


class ProductView(LoginRequiredMixin, FormView, ListView):
    paginate_by = 5
    form_class = ProductForm
    template_name = "finances/product_page.html"

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-id')
        return queryset

    def form_valid(self, form):
        self.success_url = self.request.META.get('HTTP_REFERER') or reverse('finances')
        form.save()
        return super().form_valid(form)


class TransactionView(LoginRequiredMixin, FormView, ListView):
    paginate_by = 5
    form_class = TransactionForm
    template_name = "finances/product_transaction.html"

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-id')
        return queryset

    def form_valid(self, form):
        self.success_url = self.request.META.get('HTTP_REFERER') or reverse('finances')
        form.save()
        return super().form_valid(form)

