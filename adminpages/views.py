from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import transaction, OperationalError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from payapp.models import Money, MoneyTransfer


@csrf_protect
def view_accounts(request):
    if request.user.is_superuser:
        if request.method == "POST":
            if 'make_super' in request.POST:
                try:
                    with transaction.atomic():
                        user = User.objects.select_related().get(id=request.POST.get('make_super'))
                        user.is_superuser = True
                        user.is_staff = True
                        user.save()
                        print(User.objects.select_related().get(id=request.POST.get('make_super')).is_superuser)
                        messages.info(request, f"updated")
                except OperationalError:
                    messages.info(request, f"Transfer operation is not possible now.")

        users = Money.objects.prefetch_related('name')
        return render(request, "adminpages/view_accounts.html", {"users": users})
    return redirect("home")


@csrf_protect
def view_transactions(request):
    if request.user.is_superuser:
        transactions = MoneyTransfer.objects.select_related().reverse()
        return render(request, "adminpages/view_transactions.html", {"transactions": transactions})
    return redirect("home")
