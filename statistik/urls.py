"""statistik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from statistik import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<game>(IIDX|DDR))$', views.index, name='index'),
    url(r'^ratings$', views.ratings_view, name='ratings'),
    url(r'^(?P<game>(IIDX|DDR))/ratings$', views.ratings_view, name='ratings'),
    url(r'^user$', views.user_view, name='users'),
    url(r'^user/(?P<user_id>([0-9]*))$', views.user_view, name='users'),
    url(r'^chart/(?P<chart_id>([0-9]*))$', views.chart_view, name='chart'),
    url(r'^elo$', views.elo_view, name='elo'),
    url(r'^(?P<game>(IIDX|DDR))/elo$', views.elo_view, name='elo'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^register$', views.register_view, name='register'),
    url(r'^search$', views.search_view, name='search'),
    url(r'^(?P<game>(IIDX|DDR))/search$', views.search_view, name='search'),
]

urlpatterns += staticfiles_urlpatterns()
