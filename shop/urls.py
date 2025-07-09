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
    path("basket_add/<int:pk>/", basket_add, name="basket_add"),
    path("basket_update/<int:pk>/", basket_update, name="basket_update"),
    path("basket_remove/<int:pk>/", basket_remove, name="basket_remove"),
    path("comment/<int:pk>/", add_comment, name="comment"),
    path("search/", ProductSearch.as_view(), name="search"),
    path("index_search/", IndexSearch.as_view(), name="index_search"),
    path("location/", Location.as_view(), name="location"),
    path("my-account/", MyAccount.as_view(), name="account"),
]


