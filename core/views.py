from django.views.generic import ListView, DetailView, RedirectView, TemplateView
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django_filters.views import FilterView
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserForm, ProfileForm
from django.db import transaction
from django.utils.translation import gettext as _
from finances.models import Product


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['group'] = Group.objects.all()
        return context


# class TransactionListView(LoginRequiredMixin, ListView):
# class ProductView(LoginRequiredMixin, ListView):
#     template_name = "product_page.html"
    # paginate_by = 10
    # filterset_class = AccountTransactionsFilter

    # def get(self, request, *args, **kwargs):
    #     if not request.is_ajax():
    #         return HttpResponseBadRequest()
    #     return super().get(request, *args, **kwargs)

    # def get_queryset(self):
    #     counterparty = Account.objects.only_counterparty().values_list('id', flat=True)
    #     for pk in counterparty:
    #         if pk == self.kwargs['account_id']:
    #             account = get_object_or_404(Account.objects.only_counterparty(), pk=self.kwargs['account_id'])
    #             break
    #     else:
    #         account = get_object_or_404(Account, pk=self.kwargs['account_id'])
    #     if self.request.GET['type'] == 'exchange':
    #         return Transaction.objects.filter(Q(account_balance_to__account=account) & Q(type='exchange')).order_by('-pk')
    #     elif self.request.GET['type'] == 'account':
    #         return Transaction.objects.filter(
    #             (Q(account_balance_to__account=account) & Q(type__exact='transaction') & (Q(approved=True) | Q(approved=False))) |
    #             (Q(account_balance_from__account=account) & Q(type__exact='transaction') & (Q(approved=True) | Q(approved=False)))
    #         ).order_by('-approved_date')

class ProductView(LoginRequiredMixin, TemplateView):
    template_name = "product_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['product'] = User.objects.all()
        context['group'] = Group.objects.all()
        return context


# class ProductView(LoginRequiredMixin, DetailView):
#     model = Product
#     template_name = "product_page.html"
#
#     # def get_queryset(self):
#     #     return LoggedInAccountAPIView.check_admin(self)
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductView, self).get_context_data(**kwargs)
#         # form = TransactionForm()
#
#         return context


@login_required
def about_page(request):
    return render(request, "about.html")


@login_required
def contact_page(request):
    return render(request, "contact.html")


@login_required
@transaction.atomic
def update_profile(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('home')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

