"""
URL configuration for PopularPhrases2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from pp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("vote/<int:quote_id>/<str:vote_type>/", views.vote_quote, name="vote_quote"),
    path('add-quote/', views.add_quote, name="add-quote"),
    path('top-10/', views.top, name="top"),
    path('check-title/', views.check_title_limit, name='check_title_limit'),
]
