from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'datasets', views.DataSetViewSet)
router.register(r'datafiles', views.DataFileViewSet)


urlpatterns = [
    path('datafiles/', views.DataFileList.as_view(), name='datafiles'),
    path('datasets/', views.DataSetList.as_view(), name='datasets'),
    path('api/', include(router.urls)),
    path('api/api-auth/', include('rest_framework.urls')),
    path('', views.view_home, name='home'),
]
