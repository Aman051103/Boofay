from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="market-home"),
    path("restaurant/<str:name>/", views.restaurant, name="restaurant"),
    path("menu/<str:category>/", views.foods, name="foods"),
    path("user/<str:name>/", views.customer_auth, name="customer"),
    path("user/<str:name>/profile/", views.profile, name="customer_profile"),
    path("user/<str:name>/foods/", views.food_search, name="food_search"),
    path("user/<str:name>/<str:item>food-receive-confirmation/", views.received, name="received"),

    path("user/<str:name>/H@3Lp47W!rDz2Fq1xG[9]VcYbT%nAeXoQpI)uJ!kM6lNz8RcSvDfUjXyZtEiOaBsHgFpVdWmJkLnZbQsYeXrAtUvIoCmEfGz/<str:cart>/", views.get_cart, name="getting_customer_orders"),

    path("user/<str:name>/cart/", views.cart, name="customer_orders"),
    path("place-order/", views.order_placed, name="placed_customer_orders"),
    path("login-handle/", views.login_handle, name="login"),
    path("customer-signup-handle/", views.customer_signup_handle, name="c_signup"),
]