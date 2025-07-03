from django.urls import path

from shop.views import *

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("signout/", signout, name="signout"),
]