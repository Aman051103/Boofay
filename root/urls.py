from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="root"),
    path("user/<str:name>/", views.root_user, name="root_user"),
    path("root-login-handle/", views.root_login_handle, name="root_login"),
    path("user/<str:name>/<str:restaurant>/paids/", views.paids, name="paids"),
    path("user/<str:name>/<str:item>order-paid-confirmation/<str:restaurant>/", views.now_paid, name="prepared"),
    path("user/<str:name>/<str:restaurant>/unpaids/", views.unpaids, name="unpaids"),
]