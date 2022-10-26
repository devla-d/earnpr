from django.shortcuts import render, redirect

from django.contrib import messages
from account.models import Account, Referral


from .forms import RegisterForm


def login(request):
    return render(request, "auth/login.html")


def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save()
            refcode = form.cleaned_data["referal_code"]
            if refcode:
                old_user = None
                try:
                    old_user = Account.objects.get(username__exact=refcode)
                except Account.DoesNotExist:
                    old_user = None

                print("old usere is", old_user.email, old_user.balance)

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
