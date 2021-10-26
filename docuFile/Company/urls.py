from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout',views.logout, name='logout'),
    path('issue', views.issue, name='certificate'),
    path('request', views.request, name='permission'),
    path('pending', views.pending, name='pending'),
    path('view', views.view, name='view'),
    path('certificate', views.certificate, name='certificate'),
    path('download',views.download, name='download')
]