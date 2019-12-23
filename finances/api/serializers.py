from django.contrib.auth.models import User, Group
from core.models import Profile
from rest_framework import serializers
from finances.models import Product, Transaction, Currency


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


# class ProfileForm(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('phone_number', 'city', 'street', 'birth_date', 'comment', )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TransactionSerializer(serializers.Serializer):

    sent_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    value = serializers.DecimalField(max_digits=20, decimal_places=2)
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())


    def validate(self, data):
        """
        Don't saving negative balance.
        """
        # with open('MyLog.txt', 'a', encoding='utf-8') as file:
        #     file.write('{}\n'.format(  7777  ))
        #     file.write('{}\n'.format(  data  ))
        # account_from = self.context.get('account_from')
        # account_to = data['account']
        # request = self.context.get("request")
        # if request.GET.get('add_money', '') == 'to_storage' and account_from == account_to:
        #     return data
        #
        # unconfirmed_transaction = Transaction.objects.filter(
        #     currency_from=data['currency'],
        #     account_balance_from__account=account_from,
        #     need_to_approve=True,
        #     approved=None,
        # )
        # val = 0
        # if unconfirmed_transaction:
        #     val = sum(unconfirmed_transaction.values_list('value_from', flat=True))
        #
        # case = AccountBalance.objects.filter(account=account_from, currency=data['currency']).first()
        # check_value = case.balance - data['value'] - val
        # if check_value < 0:
        #     raise serializers.ValidationError('Недостатньо коштів на рахунку!')
        return data

    def create(self, validated_data, **kwargs):
        sent_to = validated_data['sent_to']
        request = self.context.get("request")

        with open('MyLog.txt', 'a', encoding='utf-8') as file:
            file.write('{}\n'.format(  validated_data['value']  ))

        # if request.GET.get('add_money', '') == 'to_storage' and sent_from == sent_to:
        #     is_add_money = True

        obj = Transaction.objects.create(
            sent_from=request.user,
            sent_to=sent_to,
            value=validated_data['value'],
            currency=validated_data['currency'],
        )
        return obj

    # def to_representation(self, instance):
    #     account = self.context.get("account")
    #     return {
    #         'pk': instance.pk,
    #         'from': instance.account_balance_from.account.name,
    #         'to': instance.account_balance_to.account.name,
    #         'amount': instance.value_from,
    #         'sent_by': instance.sent_by.get_full_name(),
    #         'approved': instance.approved,
    #         'currency': instance.currency_from.iso_code,
    #         'html': render_to_string('finances/parts/transaction_request.html',
    #                                  context={'transaction': instance, 'account': account})
    #     }