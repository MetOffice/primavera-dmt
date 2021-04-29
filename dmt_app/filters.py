"""
Define filters to filter rows of dmt_app models using django_filters.
"""
import django_filters

from .models import DataFile


class DataFileFilter(django_filters.FilterSet):
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
        return queryset
