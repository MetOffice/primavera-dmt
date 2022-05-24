from django.contrib.auth import (authenticate, login, logout)
from django.shortcuts import render, redirect
from rest_framework import permissions, renderers, viewsets

from .filters import DataFileFilter, DataSetFilter
from .models import DataFile, DataSet
from .serializers import DataFileSerializer, DataSetSerializer
from .tables import DataFileTable, DataSetTable
from .utils.table_views import PagedFilteredTableView


class DataFileList(PagedFilteredTableView):
    model = DataFile
    table_class = DataFileTable
    filter_class = DataFileFilter
    page_title = 'Data Files'


class DataSetList(PagedFilteredTableView):
    model = DataSet
    table_class = DataSetTable
    filter_class = DataSetFilter
    page_title = 'Data Sets'


def view_home(request):
    return render(request, 'dmt_app/home.html',
                  {'request': request, 'page_title': 'PRIMAVERA DMT'})


def view_login(request):
    return render(request, 'dmt_app/login.html',
                  {'request': request, 'page_title': 'Login'})


def view_logout(request):
    # logout(request)
    return redirect('home')


class DataSetViewSet(viewsets.ModelViewSet):
    """
    Rest API viewset for datasets
    """
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filterset_fields = ['name', 'version']


class DataFileViewSet(viewsets.ModelViewSet):
    """
    Rest API viewset for datafiles
    """
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filterset_fields = ['name', 'incoming_directory', 'directory', 'online',
                        'dataset__id']
