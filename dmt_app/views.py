# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
Django views for the dmt_app
"""

# pylint: disable=too-many-ancestors

import re

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
    title_bar_text = settings.TITLE_BAR_TEXT


class DataSetList(PagedFilteredTableView):
    """Show Data sets"""

    model = DataSet
    table_class = DataSetTable
    filter_class = DataSetFilter
    page_title = "Data Sets"
    title_bar_text = settings.TITLE_BAR_TEXT


def view_home(request):
    """Show the home page"""
    return render(
        request,
        "dmt_app/home.html",
        {
            "request": request,
            "page_title": "DMT",
            "title_bar_text": settings.TITLE_BAR_TEXT,
        },
    )


class SetPagination(PageNumberPagination):
    """Control the API's pagination"""

    page_size = settings.REST_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = settings.REST_MAX_PAGE_SIZE


class DataSetViewSet(viewsets.ModelViewSet):
    """Rest API viewset for datasets"""

    queryset = DataSet.objects.all().order_by("id")
    serializer_class = DataSetSerializer
    pagination_class = SetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = ["name", "version"]

    def perform_create(self, serializer):
        """Save derived attributes on set creation in the API"""
        numerical_version = None
        version = serializer.validated_data.get("version")
        if version:
            matches = re.findall(r"(\d+(?:\.\d+)?)", version)
            if matches:
                numerical_version = matches[0]
        serializer.save(
            creator=self.request.user.username, numerical_version=numerical_version
        )


class DataFileViewSet(viewsets.ModelViewSet):
    """Rest API viewset for datafiles"""

    queryset = DataFile.objects.all().order_by("id")
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
