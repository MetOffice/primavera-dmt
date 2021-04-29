from django.urls import path

from . import views

urlpatterns = [
    path('datafiles/', views.DataFileList.as_view(), name='data_files'),
    path('datasets/', views.view_datasets, name='data_sets'),
    path('login/', views.view_login, name='login'),
    path('logout/', views.view_logout, name='logout'),
    path('', views.view_home, name='home'),
]