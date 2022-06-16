# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""Common code used by many tests"""

from dmt_app.models import DataFile, DataSet


class SampleDjangoEntities:
    """Make sample DataSet and DataFile"""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        """Create base object"""
        self.dataset = None
        self.datafile1 = None
        self.datafile2 = None
        self.dataset_attrs = {"name": "OBS", "version": "1"}
        self.datafile1_attrs = {
            "name": "file1.nc",
            "incoming_directory": "/some/dir",
            "size": 1,
            "checksum_value": "abcdef",
            "checksum_type": "MD5",
            "online": True,
        }
        self.datafile2_attrs = {
            "name": "file2.nc",
            "incoming_directory": "/other/dir",
            "size": 2,
            "checksum_value": "123456",
            "checksum_type": "SHA256",
            "online": False,
        }

    def make_django_entities(self):
        """Make sample DataSet and DataFile"""
        self.dataset = DataSet.objects.create(**self.dataset_attrs)
        self.datafile1 = DataFile.objects.create(
            dataset=self.dataset, **self.datafile1_attrs
        )
        self.datafile2 = DataFile.objects.create(
            dataset=self.dataset, **self.datafile2_attrs
        )
        return self
