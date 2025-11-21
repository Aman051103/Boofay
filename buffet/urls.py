"""buffet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

    
urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('login-page/', views.Login, name='login-page'),
    path("logout/", views.Logout, name="logout"),
    path('add-restaurant/', views.restaurant_signup, name='signup-rest'),
    path('customer-signup/', views.customer_signup, name='signup-cust'),
    path('otp-sent/', views.sent_otp, name='sent-otp'),
    path('pwd-otp-sent/', views.sent_otp_pwd, name='pwd-sent-otp'),
    path('send-otp/', views.send_otp, name='send-otp'),
    path('send-otp-pwd/', views.send_otp_pwd, name='send-otp-pwd'),
    path('otp-confirmation/', views.otp_confirmation, name='confirm-otp'),
    path('password-otp-confirmation/', views.otp_confirmation_pwd, name='confirm-otp-pwd'),
    path('change-pwd/', views.change_pwd, name='change-pwd'),
    path('market-place/', include('market_place.urls')),
    path('collab/', include('collab.urls')),
    path('root/', include('root.urls')),
    path('feeds/', include('feeds.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
