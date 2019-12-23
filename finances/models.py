from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum


class Currency(models.Model):
    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    iso_code = models.CharField(max_length=3, verbose_name=_('ISO Code'))

    def __str__(self):
        return "{} ({})".format(self.name, self.iso_code)


class AccountType(models.Model):
    class Meta:
        verbose_name = _('Account type')
        verbose_name_plural = _('Account types')

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    can_attach_to_user = models.BooleanField(
        default=False,
        verbose_name=_('Can attach to user'),
        help_text=_('Set it if this account can be attach to user')
    )
    visible_by = models.ManyToManyField(
        Group,
        verbose_name=_('Visible by'),
        help_text=_('Who sees accounts in outgoing transactions'),
        related_name='visible_accounttypes',
        blank=True
    )
    accessible_by = models.ManyToManyField(
        Group,
        verbose_name=_('Accessible by'),
        help_text=_('Who can access accounts to incoming/outgoing transactions and can see balance'),
        related_name='accessible_accounttypes',
        blank=True
    )

    def __str__(self):
        return self.name


class Account(models.Model):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    type = models.ForeignKey(AccountType, on_delete=models.PROTECT, verbose_name=_('Type'))

    def __str__(self):
        return self.name


class AccountBalance(models.Model):
    class Meta:
        unique_together = (('account', 'currency'),)

    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('Account'), related_name='balances')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name=_('Currency'))
    balance = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('Balance'))

    def __str__(self):
        return "{}: {}{}".format(self.account.name, self.balance, self.currency.iso_code)


class ProductProvider(models.Model):
    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')

    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    provider = models.ForeignKey(ProductProvider, on_delete=models.PROTECT, verbose_name=_('Provider'))
    cost = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('Сost'))
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name=_('Currency'))

    def __str__(self):
        return "{} (виробник: {}), вартість {}{}".format(self.name, self.provider, self.cost, self.currency.iso_code)


class Transaction(models.Model):
    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    STATUSES = (
        ('buy', 'Купівля'),
        ('sale', 'Продаж'),
    )

    account_balance = models.ForeignKey(AccountBalance, on_delete=models.CASCADE,
                                        related_name='account_balance')
    new_balance = models.DecimalField(null=True, blank=True, default=None, max_digits=20, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product')
    value = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='currency')
    surcharge = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True,
                                    verbose_name=_('Surcharge'))
    sent_from = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sent_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='sent_transactions', )
    type = models.CharField(max_length=15, choices=STATUSES, default="sale")
    created_at = models.DateTimeField(auto_now_add=True)
    is_refund = models.BooleanField(default=False)

    # def save(self, **kwargs):
    #
    #     with open('MyLog.txt', 'a', encoding='utf-8') as file:
    #         file.write('9999''{}\n'.format(  'SAVE METHOD'  ))
        # with transaction.atomic():
        #     if not self.need_to_approve and not self.pk:
        #         self.account_balance_from.balance -= self.value_from
        #         self.account_balance_from.save()
        #         if self.account_balance_to.currency.iso_code == 'UAH':
        #             self.account_balance_to.balance += (self.value_to - self.short_change)
        #         elif self.account_balance_from.currency.iso_code != 'UAH':
        #             self.account_balance_to.balance += self.value_to
        #             if self.short_change:
        #                 self.account_uah_balance.balance -= self.short_change
        #                 self.account_uah_balance.save()
        #             if self.surcharge:
        #                 self.account_uah_balance.balance += self.surcharge
        #                 self.account_uah_balance.save()
        #         else:
        #             self.account_balance_to.balance += self.value_to
        #         self.account_balance_to.save()
        #         self.new_balance_from = self.account_balance_from.balance
        #         self.new_balance_to = self.account_balance_to.balance
        #     self.daily_number_increment()
        #     super().save(**kwargs)

    def __str__(self):
        return "Ініціатор - {}, кому - {}, {} товар - '{}', продано за:{}{}, дохід:{}{} ".format(self.sent_from, self.sent_to, self.type, self.product, self.value,
                                                               self.currency.iso_code, self.surcharge, self.currency.iso_code)
