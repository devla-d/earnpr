from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_str
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


def changePassword(request):
    if request.POST:
        email = request.POST.get("email")
        try:
            user = Account.objects.get(email__exact=email)
        except Account.DoesNotExist:
            user = None

        if user:
            current_site = get_current_site(request)
            subject = f"Reset password {current_site.domain}"
            context = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
            message = get_template("auth/resetPasswordemail.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[user.email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            messages.info(request, "Check your mail box for instructions")
            return redirect("forgot-password")
        else:
            messages.info(request, "A user with this email does not exist")
            return redirect("forgot-password")
    return render(request, "auth/changePassword.html")


def resetPassword(request):
    uidb64 = request.GET.get("uid")
    token = request.GET.get("token")
    print(uidb64, token)
    if token and uidb64:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if request.POST:
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()

                    messages.info(request, "Password change")
                    return redirect("login")
            else:
                form = SetPasswordForm(user=user)
            return render(request, "auth/resetPassword.html", {"form": form})
        else:
            messages.warning(
                request,
                ("Link is invalid."),
            )
            return redirect("forgot-password")

    else:
        messages.warning(
            request,
            (
                "The confirmation link is invalid, possibly because it has already been used."
            ),
        )
        return redirect("forgot-password")
