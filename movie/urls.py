"""movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/push/', core_views.push),
    path('', core_views.user_login),
    path('index/', core_views.index),
    path('user/register/', core_views.user_register),
    path('user/logout/', core_views.user_logout),
    path('type/<str:movietype>/', core_views.movietype),
    path('movie/detail/<int:movie_id>/', core_views.movie_detail),
    path('movie/score/<int:score>/<int:movie_id>/', core_views.movie_score),
    path('profile/<int:user_id>/', core_views.profile),
    path('search/', core_views.search),
    path('movie/recommend/<int:movie_id>/', core_views.movie_recommend),
    path('movie/ur/<int:uid>/', core_views.movie_recommend_uid)
]
