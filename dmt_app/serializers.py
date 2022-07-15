# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

# pylint: disable=missing-class-docstring
"""
Serialize the models for the REST API
"""

from rest_framework import serializers

from .models import DataFile, DataSet


class DataSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataSet
        fields = (
            "id",
            "name",
            "version",
            "url",
            "summary",
            "doi",
            "reference",
            "license",
            "date_downloaded",
            "datafile_set",
        )


class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataFile
        fields = (
            "id",
            "name",
            "incoming_directory",
            "directory",
            "size",
            "checksum_value",
            "checksum_type",
            "online",
            "size",
            "checksum_value",
            "checksum_type",
            "time_units",
            "calendar",
            "start_time",
            "end_time",
            "frequency",
            "standard_name",
            "long_name",
            "var_name",
            "units",
            "dimensions",
            "dataset",
        )  # pylint: disable=duplicate-code
