"""Cosmoz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from Accounts import views as account_views
from Home.views import HomePage
from Forum import views as forum_views


app_name = [
    "Accounts",
    "Connect",
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePage, name="home"),
    path("signup/", account_views.SignUpView, name="SignUp"),
    path("login/", account_views.LoginView, name="Login"),
    path("logout/", account_views.LogoutView, name="Logout"),
    path("accounts/", include("Accounts.urls")),
    path("search/", account_views.account_search_view, name="search"),
    path("connect/", include("Connect.urls", namespace="friend")),
    path("dashboard/", include("Dashboard.urls")),
    path("forum/", include("Forum.urls")),
    path("forum/search_questions/",forum_views.SearchView.as_view(),name="search-question"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
