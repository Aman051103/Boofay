from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="collab-home"),
    path("restaurant/admin/<str:name>/", views.restaurant_auth, name="rest_admin"),
    path("restaurant/admin/<str:name>/my-foods/", views.my_foods, name="my_foods"),
    path("restaurant/admin/<str:name>/add-foods/", views.add_foods, name="add_foods"),
    path("restaurant/admin/<str:name>/item-added/", views.item_added, name="item-added"),
    path("restaurant/admin/<str:name>/data/", views.payment_data, name="payment_data"),
    path("restaurant-signup-handle/", views.restaurant_signup_handle, name="r_signup"),
    path("restaurant/admin/<str:name>/profile/", views.profile, name="rest_profile"),
    path("restaurant/admin/<str:name>/<str:item>food-prepared-confirmation/", views.prepared, name="prepared"),
    path("restaurant/admin/<str:name>/<str:item>/alter-item-availability/", views.stock, name="availability"),
]