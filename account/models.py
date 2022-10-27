from email.policy import default
from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.models import AbstractUser


def genarateRefId():
    uniqueId = get_random_string(6, "abcdef0123456789").upper()
    return uniqueId


class Account(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    zipcode = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    fullname = models.CharField(max_length=100, blank=True, null=True)

    address = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)

    city = models.CharField(max_length=100, blank=True, null=True)

    date_of_birth = models.CharField(max_length=100, blank=True, null=True)

    phone = models.CharField(max_length=30, blank=True, null=True, unique=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
    deposit_balance = models.IntegerField(default=0, blank=True, null=True)

    total_withdraw = models.IntegerField(default=0, blank=True, null=True)
    referral_bonus = models.IntegerField(default=0, blank=True, null=True)
    referral = models.IntegerField(default=0, blank=True, null=True)

    unique_id = models.CharField(max_length=30, unique=True, default=genarateRefId())

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Referral(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="ref_user")
    referred_by = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="ref_by_user",
        null=True,
        blank=True,
    )
    referrals = models.ManyToManyField(Account, related_name="my_referrals")

    def __str__(self):
        return self.user.username


class LoginHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="log_user")
    log_ip = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.log_ip}"
