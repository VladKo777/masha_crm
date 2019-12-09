from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, RedirectView, TemplateView, FormView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm


@login_required
def finances(request):
    return render(request, "finances.html")


class ProductView(LoginRequiredMixin, FormView):
    form_class = ProductForm
    template_name = "product_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

    def form_valid(self, form):
        self.success_url = self.request.META.get('HTTP_REFERER') or reverse('finances')
        form.save()
        return super().form_valid(form)


# class ProductView(LoginRequiredMixin, TemplateView):
#     template_name = "product_page.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductView, self).get_context_data(**kwargs)
#         context['form'] = ProductForm()
#         context['products'] = Product.objects.all()
#         return context
