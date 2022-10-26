from django.urls import path
from . import views

urlpatterns = [
    path("dasboard/", views.dashboard, name="dashbaord"),
    path("history/", views.history, name="history"),
    path("withdraw-funds/", views.withdraw, name="withdraw"),
    path("referals/", views.referals, name="referals"),
    path("account-details/", views.settings, name="settings"),
]
