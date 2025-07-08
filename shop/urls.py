from django.urls import path

from shop.views import *

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("category/<int:pk>", ProductByCategory.as_view(), name="category"),
    path("product/<int:pk>", ProductDetail.as_view(), name="detail"),
    path("likes/", LikeList.as_view(), name="likes"),
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("signout/", signout, name="signout"),
    path("contact/", contact, name="contact"),
    path("likes/<int:pk>/", user_like, name="like"),
    path("basket/", basket, name="basket"),
]