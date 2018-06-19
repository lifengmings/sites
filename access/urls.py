from django.urls import path
from access import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('pre_open_door', views.pre_opendoor, name='pre_open_door'),
    path('open_door/', views.opdoor, name='open_door'),
]