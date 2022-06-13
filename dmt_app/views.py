# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
Django views for the dmt_app
"""

# pylint: disable=too-many-ancestors

from django.shortcuts import render
from django.conf import settings
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .filters import DataFileFilter, DataSetFilter
from .models import DataFile, DataSet
from .serializers import DataFileSerializer, DataSetSerializer
from .tables import DataFileTable, DataSetTable
from .utils.table_views import PagedFilteredTableView


class DataFileList(PagedFilteredTableView):
    """Show Data files"""

    model = DataFile
    table_class = DataFileTable
    filter_class = DataFileFilter
    page_title = "Data Files"


class DataSetList(PagedFilteredTableView):
    """Show Data sets"""

    model = DataSet
    table_class = DataSetTable
    filter_class = DataSetFilter
    page_title = "Data Sets"


def view_home(request):
    """Show the home page"""
    return render(
        request, "dmt_app/home.html", {"request": request, "page_title": "DMT"}
    )


class SetPagination(PageNumberPagination):
    """Control the API's pagination"""

    page_size = settings.REST_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = settings.REST_MAX_PAGE_SIZE


class DataSetViewSet(viewsets.ModelViewSet):
    """Rest API viewset for datasets"""

    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    pagination_class = SetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = ["name", "version"]

    def perform_create(self, serializer):
        """Save the username on set creation in the API"""
        serializer.save(creator=self.request.user.username)


class DataFileViewSet(viewsets.ModelViewSet):
    """Rest API viewset for datafiles"""

    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    pagination_class = SetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = [
        "name",
        "incoming_directory",
        "directory",
        "online",
        "dataset__id",
    ]
