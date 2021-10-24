from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout',views.logout, name='logout'),
    path('pending', views.pending, name='pending'),
    path('granted', views.granted, name='granted'),
    path('request', views.request, name='request'),
    path('home', views.home, name='home'),
    path('download',views.download, name='download')
]