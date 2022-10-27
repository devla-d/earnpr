from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("register/done/", views.registerDone, name="registerDone"),
]
