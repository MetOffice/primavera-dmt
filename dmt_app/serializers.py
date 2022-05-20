"""
Serialize the models for the REST API
"""

from rest_framework import serializers

from .models import DataFile, DataSet


class DataSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataSet
        fields = ('name', 'version', 'url', 'summary', 'doi', 'reference', 'license',
                  'date_downloaded', 'datafiles')


class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataFile
        fields = ('name', 'incoming_directory', 'directory', 'size', 'checksum_value',
                  'checksum_type', 'online', 'dataset')
