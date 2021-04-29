from django.contrib.auth import (authenticate, login, logout)
from django.shortcuts import render, redirect

from .filters import DataFileFilter
from .models import DataFile
from .tables import DataFileTable
from .utils.table_views import PagedFilteredTableView


class DataFileList(PagedFilteredTableView):
    model = DataFile
    table_class = DataFileTable
    filter_class = DataFileFilter
    page_title = 'Data Files'

def view_datasets(request):
    return render(request, 'dmt_app/dataset_list.html',
                  {'request': request, 'page_title': 'Data Sets'})

def view_home(request):
    return render(request, 'dmt_app/home.html',
                  {'request': request, 'page_title': 'PRIMAVERA DMT'})

def view_login(request):
    return render(request, 'dmt_app/login.html',
                  {'request': request, 'page_title': 'Login'})

def view_logout(request):
    # logout(request)
    return redirect('home')