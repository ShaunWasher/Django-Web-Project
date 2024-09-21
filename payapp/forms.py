from django import forms
from . import models


class SendMoneyForm(forms.ModelForm):

    class Meta:
        model = models.MoneyTransfer
        fields = ["enter_destination_username", "enter_money_to_transfer"]


class RequestMoneyForm(forms.ModelForm):

    class Meta:
        model = models.PayRequest
        fields = ["enter_destination_username", "enter_money_to_transfer"]
