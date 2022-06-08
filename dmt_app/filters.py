# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
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
        fields = ['name', 'directory', 'dataset', 'online']

    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    directory = django_filters.CharFilter(field_name='directory',
                                          lookup_expr='icontains')

    dataset = django_filters.NumberFilter(
        field_name='dataset__id'
    )

    def filter_online(self, queryset, name, value):
        if value:
            return queryset.filter(online=True)
        else:
            return queryset


class DataSetFilter(django_filters.FilterSet):
    """
    Filter for dmt_app.models.DataSet
    """
    class Meta:
        model = DataSet
        fields = ['name', 'version']

    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    version = django_filters.CharFilter(field_name='version',
                                        lookup_expr='icontains')
