from django.shortcuts import render


def dashboard(request):
    return render(request, "users/index.html")


def history(request):
    return render(request, "users/history.html")


def withdraw(request):
    return render(request, "users/withdraw.html")


def referals(request):
    return render(request, "users/referrals.html")


def settings(request):
    return render(request, "users/settings.html")
