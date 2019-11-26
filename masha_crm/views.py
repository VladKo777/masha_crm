from django.http import HttpResponse
import datetime
from django.db.models import Count, Sum
from django.utils import timezone
from finances.models import Account
from django.views.generic import ListView, DetailView, RedirectView, TemplateView
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django_filters.views import FilterView
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm


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


class HomeTemplateView(LoginRequiredMixin, FilterView, TemplateView):
    filterset_class = AccountTransactionsFilter
    template_name = "home_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['Users'] = User.objects.all()
        context['Group'] = Group.objects.all()

        return context

    # def get_context_data(self, *args, **kwargs):
    #     context = super(HomeTemplateView, self).get_context_data(**kwargs)
    #     # is_logged = ExchangerLogin.objects.is_logged(self.request.user)
    #     # account = is_logged.account
    #     # context['account'] = account
    #     #
    #     # t = timezone.now()
    #     # context['today_date'] = t.date()
    #     # today_start = timezone.now() - datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    #     # today_transactions = Transaction.objects.filter(created_at__gt=today_start, type='exchange',
    #     #                                                 account_balance_from__account=account,
    #     #                                                 account_balance_to__account=account)
    #     #
    #     # total_buy_today = today_transactions.values('currency_to').annotate(total_amount=Sum('value_to'))
    #     # total_sold_today = today_transactions.values('currency_from').annotate(total_amount=Sum('value_from'))
    #     # context['total_buy_today'] = total_buy_today
    #     # context['total_sold_today'] = total_sold_today
    #     #
    #     # total_buy_and_sold_by_rate = today_transactions.values('currency_to', 'currency_from', 'rate').annotate(
    #     #     total_amount_buy=Sum('value_to'), total_amount_sold=Sum('value_from'))
    #     # context['total_buy_and_sold_by_rate'] = total_buy_and_sold_by_rate
    #     #
    #     # currencies = Currency.objects.values('id', 'iso_code')
    #     # context['currencies'] = currencies
    #     return context


@login_required
def about_page(request):
    return render(request, "about.html")

@login_required
def contact_page(request):
    return render(request, "contact.html")
