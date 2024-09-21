import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from payapp.models import Money


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    currency = forms.ChoiceField(choices=(('£', 'GB Pounds'), ('$', 'US Dollars'), ('€', 'Euros')))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "currency", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegisterForm, self).__init__(*args, **kwargs)

    def get_base_url(self):
        if self.request:
            return self.request.scheme + "://" + self.request.get_host()
        return None

    def save(self, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)
        Money.objects.create(name=instance, money=1000*float(requests.get(self.get_base_url()+"/conversion/£/"+self.cleaned_data['currency']).text),
                             currency=self.cleaned_data['currency'])
        return instance
