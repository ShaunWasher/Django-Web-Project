import requests
from django.contrib.auth.models import User
from django.db import transaction, OperationalError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from payapp.forms import SendMoneyForm, RequestMoneyForm
from payapp.models import Money, MoneyTransfer, PayRequest


@csrf_protect
def home(request):
    if request.method == "POST":  # if there is a post request it should be accepting or rejecting payment requests
        if 'reject' in request.POST:
            try:
                with transaction.atomic():
                    PayRequest.objects.select_related().get(id=request.POST.get('reject')).delete()
            except OperationalError:
                messages.info(request, f"Transfer operation is not possible now.")
        elif 'pay' in request.POST:
            payment_request = PayRequest.objects.select_related().get(id=request.POST.get('pay'))
            dst_money = Money.objects.select_related().get(name__username=payment_request.enter_your_username)
            src_money = Money.objects.select_related().get(name__username=payment_request.enter_destination_username)
            money_to_transfer = float(payment_request.enter_money_to_transfer)
            try:
                with transaction.atomic():
                    src_money.money = float(src_money.money) - money_to_transfer*float(requests.get(request.scheme + "://" + request.get_host() + "/conversion/"+dst_money.currency+"/"+src_money.currency+"/").text)
                    src_money.save()

                    dst_money.money = float(dst_money.money) + money_to_transfer
                    dst_money.save()

                    MoneyTransfer.objects.create(enter_your_username=payment_request.enter_destination_username,
                                                 enter_destination_username=payment_request.enter_your_username,
                                                 enter_money_to_transfer=money_to_transfer,
                                                 currency=dst_money.currency)
                    payment_request.delete()
            except OperationalError:
                messages.info(request, f"Transfer operation is not possible now.")
            messages.info(request, "transaction complete")

    if not request.user.is_authenticated:
        return render(request, "payapp/home.html")
    user_money = Money.objects.select_related().get(name__username=request.user)
    sent_requests = PayRequest.objects.filter(enter_your_username=request.user).reverse()
    pending_requests = PayRequest.objects.filter(enter_destination_username=request.user).reverse()

    return render(request, "payapp/home.html", {'user_money': user_money, 'sent_requests': sent_requests,
                                                'pending_requests': pending_requests})


@csrf_protect
def transactions(request):
    if request.user.is_authenticated:
        user_money = Money.objects.select_related().get(name__username=request.user)
        user_transactions = MoneyTransfer.objects.filter(Q(enter_your_username=request.user) |
                                                         Q(enter_destination_username=request.user)).reverse()
        return render(request, "payapp/transactions.html",
                      {'user_money': user_money, 'user_transactions': user_transactions})
    messages.error(request, "not logged in")
    return redirect("home")


@csrf_protect
def send_money(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SendMoneyForm(request.POST)

            if form.is_valid():

                dst_username = form.cleaned_data["enter_destination_username"]
                if User.objects.filter(username=dst_username).exists():
                    if dst_username != request.user.username:

                        money_to_transfer = float(form.cleaned_data["enter_money_to_transfer"])

                        src_money = Money.objects.select_related().get(name__username=request.user.username)
                        dst_money = Money.objects.select_related().get(name__username=dst_username)

                        try:
                            with transaction.atomic():
                                src_money.money = float(src_money.money) - money_to_transfer
                                src_money.save()

                                dst_money.money = float(dst_money.money) + money_to_transfer*float(requests.get(request.scheme + "://" + request.get_host()+"/conversion/"+src_money.currency+"/"+dst_money.currency).text)
                                dst_money.save()

                                MoneyTransfer.objects.create(enter_your_username=request.user.username,
                                                             enter_destination_username=dst_username,
                                                             enter_money_to_transfer=money_to_transfer,
                                                             currency=src_money.currency)
                        except OperationalError:
                            messages.info(request, f"Transfer operation is not possible now.")
                        messages.info(request, "money sent")
                    else:
                        messages.error(request, "Cannot send money to yourself!")
                        return render(request, "payapp/send_money.html", {"form": form})
                else:
                    messages.error(request, "User Doesn't exist")
                    return render(request, "payapp/send_money.html", {"form": form})

        form = SendMoneyForm()
        return render(request, "payapp/send_money.html", {"form": form})

    messages.error(request, "not logged in")
    return redirect("home")


@csrf_protect
def request_money(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RequestMoneyForm(request.POST)

            if form.is_valid():

                dst_username = form.cleaned_data["enter_destination_username"]
                if User.objects.filter(username=dst_username).exists():
                    if dst_username != request.user.username:

                        money_to_transfer = float(form.cleaned_data["enter_money_to_transfer"])

                        src_money = Money.objects.select_related().get(name__username=request.user.username)

                        try:
                            with transaction.atomic():
                                PayRequest.objects.create(enter_your_username=request.user.username,
                                                          enter_destination_username=dst_username,
                                                          enter_money_to_transfer=money_to_transfer,
                                                          currency=src_money.currency)
                        except OperationalError:
                            messages.info(request, f"Transfer operation is not possible now.")
                        messages.info(request, "request sent")
                    else:
                        messages.error(request, "Cannot request money from yourself!")
                        return render(request, "payapp/send_money.html", {"form": form})
                else:
                    messages.error(request, "User Doesn't exist")
                    return render(request, "payapp/request_money.html", {"form": form})

        form = RequestMoneyForm()
        return render(request, "payapp/request_money.html", {"form": form})

    messages.error(request, "not logged in")
    return redirect("home")
