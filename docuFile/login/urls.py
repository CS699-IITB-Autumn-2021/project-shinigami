from django.urls import path
from . import views

# the urls that the pages get redirected to
urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.register, name='register'),
    path('auth/', views.auth_view),
    path('invalidlogin/', views.invalidlogin),
]