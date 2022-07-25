# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
Define filters to filter rows of dmt_app models using django_filters.
"""
import django_filters

from .models import DataFile, DataSet


class DataFileFilter(django_filters.FilterSet):
    """
    Filter for dmt_app.models.DataFile
    """

    class Meta:
        model = DataFile
        fields = [
            "name",
            "directory",
            "dataset_id",
            "dataset_name",
            "online",
            "project",
            "variables",
        ]

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    directory = django_filters.CharFilter(
        field_name="directory", lookup_expr="icontains"
    )

    dataset_id = django_filters.NumberFilter(field_name="dataset__id")

    dataset_name = django_filters.CharFilter(
        field_name="dataset__name", lookup_expr="icontains"
    )

    project = django_filters.CharFilter(
        field_name="dataset__project", lookup_expr="icontains"
    )

    variables = django_filters.CharFilter(method="filter_variables")

    def filter_online(self, queryset, name, value):
        """Allow filtering of online status"""
        # pylint: disable=unused-argument, no-else-return, no-self-use
        if value:
            return queryset.filter(online=True)
        else:
            return queryset

    def filter_variables(self, queryset, name, value):
        """Allow filtering of the three variable components in single filter"""
        # pylint: disable=unused-argument, no-self-use
        if not value:
            return queryset
        standard_name_qs = queryset.filter(standard_name__icontains=value)
        long_name_qs = queryset.filter(long_name__icontains=value)
        var_name_qs = queryset.filter(var_name__icontains=value)
        # Cannot use union as distinct() is called in table_views.py
        return standard_name_qs | long_name_qs | var_name_qs


class DataSetFilter(django_filters.FilterSet):
    """
    Filter for dmt_app.models.DataSet
    """

    class Meta:
        model = DataSet
        fields = ["name", "version", "project"]

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    version = django_filters.CharFilter(field_name="version", lookup_expr="icontains")

    project = django_filters.CharFilter(field_name="project", lookup_expr="icontains")
