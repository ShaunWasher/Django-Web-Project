from django.contrib.auth.models import User
from django.db import models


class Money(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    money = models.DecimalField(default=1000, decimal_places=2, max_digits=14)
    currency = models.CharField(max_length=1, default='£')  # £,$,€

    def __str__(self):
        details = ''
        details += f'Name        : {self.name}\n'
        details += f'Money      : {self.currency}{self.money}\n'
        return details


class MoneyTransfer(models.Model):
    enter_your_username = models.CharField(max_length=50)
    enter_destination_username = models.CharField(max_length=50)
    enter_money_to_transfer = models.DecimalField(decimal_places=2, max_digits=14)
    currency = models.CharField(max_length=1, default='£')  # £,$,€

    def __str__(self):
        details = ''
        details += f'username                   : {self.enter_your_username}\n'
        details += f'destination_username       : {self.enter_destination_username}\n'
        details += f'transfer_amount            : {self.currency}{self.enter_money_to_transfer}\n'
        return details


class PayRequest(MoneyTransfer):
    def __str__(self):
        details = ''
        details += f'username                   : {self.enter_your_username}\n'
        details += f'destination_username       : {self.enter_destination_username}\n'
        details += f'request_amount            : {self.currency}{self.enter_money_to_transfer}\n'
        return details
