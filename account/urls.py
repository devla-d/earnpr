from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("register/done/", views.registerDone, name="registerDone"),
]
