from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

from django.contrib import messages
from account.models import Account, Referral

from baseapp import utils
from .forms import RegisterForm, LoginForm


def login_(request):
    destination = utils.get_next_destination(request)
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"], password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                if destination:
                    return redirect(f"{destination}")
                else:
                    return redirect("dashbaord")
        else:
            messages.warning(request, ("Invalid Username Or Password."))
            return redirect("login")
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


def sign_out(request):
    messages.warning(request, "logged out")
    logout(request)
    return redirect("login")


def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save()
            refcode = form.cleaned_data["referal_code"]
            if refcode:

                old_user = None
                try:
                    old_user = Account.objects.get(unique_id__exact=refcode)
                except Account.DoesNotExist:
                    old_user = None

                if old_user:
                    oldRef = Referral.objects.get(user=old_user)
                    newRef = Referral.objects.get(user=instance)
                    oldRef.referrals.add(instance)
                    old_user.referral_bonus += 10
                    old_user.referral += 1
                    old_user.save()
                    newRef.referred_by = old_user
                    newRef.save()
                    instance.save()
                    messages.info(request, "Account created")
                    return redirect("registerDone")
                else:
                    messages.info(request, "AN UNKNOWN ERROR OCCURED")
                    return redirect("registerDone")
            else:
                messages.info(request, "Account created")
                return redirect("registerDone")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form": form})


def registerDone(request):
    return render(request, "auth/registerDone.html")
