from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, RedirectView, TemplateView, FormView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm, TransactionForm


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

