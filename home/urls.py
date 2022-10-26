import imp
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("news/", views.news, name="news"),
    path("support/", views.support, name="support"),
]
