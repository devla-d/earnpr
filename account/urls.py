from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_, name="login"),
    path("logout/", views.sign_out, name="logout"),
    path("register/", views.register, name="register"),
    path("register/done/", views.registerDone, name="registerDone"),
    path("forgot-password/", views.changePassword, name="forgot-password"),
]
