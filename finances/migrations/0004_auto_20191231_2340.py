# Generated by Django 2.1.7 on 2019-12-31 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0003_auto_20191215_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='account_balance',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='new_balance',
        ),
    ]
