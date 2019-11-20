from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# from .forms import ExchangerForm
from .models import Currency, Account, AccountType, AccountBalance, ProductProvider, Product


admin.site.register(Currency)
admin.site.register(AccountType)
admin.site.register(Product)
admin.site.register(ProductProvider)



class AccountBalanceInlineAdmin(admin.StackedInline):
    verbose_name = _('Balance')
    model = AccountBalance


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = (AccountBalanceInlineAdmin,)

