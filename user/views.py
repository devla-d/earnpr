from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from baseapp import utils

from .models import Transactions, Bank
from account.models import Referral


@login_required()
def dashboard(request):
    return render(request, "users/index.html")


@login_required()
def history(request):
    user = request.user
    transactions = Transactions.objects.filter(user=user).order_by("-date")
    return render(request, "users/history.html", {"transactions": transactions})


@login_required()
def withdraw(request):
    user = request.user
    if request.POST:
        accountnum = request.POST.get("accountnum")
        accountname = request.POST.get("accountname")
        bank = request.POST.get("bank")
        amount = int(request.POST.get("amount"))

        if user.balance >= amount:
            bank = Bank.objects.create(
                acc_name=accountname, acc_num=accountnum, ty_pe=bank
            )
            transaction = Transactions.objects.create(
                user=user,
                amount=amount,
                trans_type=utils.W,
                unique_u=utils.user_unique_id(),
            )
            transaction.bank_details = bank
            user.balance -= amount
            user.save()
            transaction.save()
            messages.success(request, ("Withdrawal Placed !"))
            return redirect("withdraw")
        else:
            messages.warning(request, ("Insufficient Funds!"))
            return redirect("withdraw")
    return render(request, "users/withdraw.html")


@login_required()
def referals(request):
    user = request.user
    ref = get_object_or_404(Referral, user=user)
    return render(request, "users/referrals.html", {"ref": ref})


@login_required()
def settings(request):
    return render(request, "users/settings.html")
