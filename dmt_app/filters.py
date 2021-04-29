import django_filters

from .models import DataFile

class DataFileFilter(django_filters.FilterSet):
    class Meta:
        model = DataFile
        fields = ['name', 'directory', 'dataset']

    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    directory = django_filters.CharFilter(field_name='directory',
                                          lookup_expr='icontains')

    dataset = django_filters.NumberFilter(
        field_name='dataset__id'
    )
