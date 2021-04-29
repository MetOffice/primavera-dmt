from django.template.defaultfilters import filesizeformat
import django_tables2 as tables

from .models import DataFile

# The string to display if a value doesn't exist
DEFAULT_VALUE = '—'


class DataFileTable(tables.Table):
    class Meta:
        model = DataFile
        attrs = {'class': 'paleblue'}
        exclude = ('id', 'incoming_directory', 'dataset', 'checksum_value',
                   'checksum_type')
        sequence = ['name', 'directory', 'online', 'size', 'checksum']

    checksum = tables.Column(empty_values=(), verbose_name='Checksum',
                             orderable=False)

    def render_checksum(self, record):
        return f'{record.checksum_type}: {record.checksum_value}'

    def render_size(self, value):
        return filesizeformat(value)
