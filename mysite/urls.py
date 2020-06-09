from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.signup, name='signup'),
    path('writedata', views.attendance, name='attendance'),
    path('post', views.display, name='display'),
    path('about', views.about, name='about'),

]
