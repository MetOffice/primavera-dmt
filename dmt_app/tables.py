"""
Define tables to display dmt_app models using django_tables2.
"""
from urllib.parse import urlencode

from django.template.defaultfilters import filesizeformat
from django.utils.html import format_html
from django.urls import reverse
import django_tables2 as tables

from .models import DataFile, DataSet

# The string to display if a value doesn't exist
DEFAULT_VALUE = '—'


class DataFileTable(tables.Table):
    """
    Table to display dmt_app.models.DataFile
    """
    class Meta:
        model = DataFile
        attrs = {'class': 'paleblue'}
        exclude = ('id', 'incoming_directory', 'dataset', 'checksum_value',
                   'checksum_type')
        sequence = ['name', 'directory', 'online', 'size', 'checksum']
        order_by = 'name'

    checksum = tables.Column(empty_values=(), verbose_name='Checksum',
                             orderable=False)

    def render_checksum(self, record):
        return f'{record.checksum_type}: {record.checksum_value}'

    def render_size(self, value):
        return filesizeformat(value)


class DataSetTable(tables.Table):
    """
    Table to display dmt_app.models.DataSet
    """
    class Meta:
        model = DataSet
        attrs = {'class': 'paleblue'}
        exclude = ('id',)
        sequence = ['name', 'version', 'num_files', 'online_status','summary',
                    'url', 'doi','license', 'reference', 'date_downloaded']
        order_by = 'name'

    num_files = tables.Column(empty_values=(), verbose_name='# Data Files',
                              orderable=False)
    online_status = tables.Column(empty_values=(), orderable=False)

    def render_num_files(self, record):
        num_datafiles = record.datafile_set.count()
        url_query = urlencode({
            'dataset': record.id,
            'dataset_string': f"{record.name} ({record.version})"
        })
        return format_html('<a href="{}?{}">{}</a>'.format(
            reverse('datafiles'),
            url_query,
            num_datafiles
        ))
