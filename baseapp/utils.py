from http.client import HTTP_PORT
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template


from uuid import uuid4
from django.contrib.auth import get_user_model


User = get_user_model()


EMAIL_ADMIN = settings.DEFAULT_FROM_EMAIL
D = "DEPOSIT"
W = "WITHDRAW"
PED = "PENDING"
ACT = "ACTIVE"
SUC = "SUCCESS"
DEC = "DECLINED"


def get_next_destination(request):
    next = None
    if request.GET.get("next"):
        next = str(request.GET.get("next"))
    return next


def earnings(amount, perc):
    p = (perc / 100) * amount
    return p + amount


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def user_unique_id():
    code = str(uuid4()).replace(" ", "").upper()[:7]
    return code


def send_regMail(user):
    subject = "Account registered successful"
    context = {
        "user": user,
    }
    message = get_template("auth/welcomail.html").render(context)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=EMAIL_ADMIN,
        to=[user.email],
        reply_to=[EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=True)
