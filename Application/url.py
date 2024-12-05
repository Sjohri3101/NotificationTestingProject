from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.indexpage, name='indexpage'),
    path('submit', views.submit, name='submit'),
    path('old', views.old, name='old'),
]