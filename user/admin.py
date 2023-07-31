from django.contrib import admin
from .models import Bank,Packages,Transactions

admin.site.register(Bank)
admin.site.register(Packages)
admin.site.register(Transactions)
