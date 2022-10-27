import imp
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def dashboard(request):
    return render(request, "users/index.html")


@login_required()
def history(request):
    return render(request, "users/history.html")


@login_required()
def withdraw(request):
    return render(request, "users/withdraw.html")


@login_required()
def referals(request):
    return render(request, "users/referrals.html")


@login_required()
def settings(request):
    return render(request, "users/settings.html")
