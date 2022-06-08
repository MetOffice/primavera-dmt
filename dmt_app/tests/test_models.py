# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
Unit tests for the dmt_app models.
"""
from django.test import TestCase

from dmt_app.models import DataFile, DataSet


class TestDataSet(TestCase):
    """Test the DataSet model"""

    def setUp(self):
        self.first_file_params = {
            "name": "obs_day_OBS-1_1deg_197801_199912.nc",
            "incoming_directory": "/some/dir",
            "directory": "/some/dir",
            "online": True,
            "size": 1,
        }
        self.second_file_params = {
            "name": "obs_day_OBS-1_1deg_200012_201812.nc",
            "incoming_directory": "/some/dir",
            "directory": "/some/dir",
            "online": True,
            "size": 2,
        }

    def test_dataset_creation(self):
        ds = DataSet.objects.create(name="OBS", version="1")
        self.assertEqual(ds.name, "OBS")
        self.assertEqual(ds.version, "1")

    def test_add_file(self):
        ds = DataSet.objects.create(name="OBS", version="1")
        df = DataFile.objects.create(dataset=ds, **self.first_file_params)
        df.save()
        self.assertEqual(ds.datafile_set.count(), 1)

    def test_status_online(self):
        ds = DataSet.objects.create(name="OBS", version="1")
        df = DataFile.objects.create(dataset=ds, **self.first_file_params)
        df.save()
        df = DataFile.objects.create(dataset=ds, **self.second_file_params)
        df.save()
        self.assertEqual(ds.online_status, "online")

    def test_status_partial(self):
        ds = DataSet.objects.create(name="OBS", version="1")
        df = DataFile.objects.create(dataset=ds, **self.first_file_params)
        df.save()
        df = DataFile.objects.create(dataset=ds, **self.second_file_params)
        df.online = False
        df.save()
        self.assertEqual(ds.online_status, "partial")

    def test_status_offline(self):
        ds = DataSet.objects.create(name="OBS", version="1")
        df = DataFile.objects.create(dataset=ds, **self.first_file_params)
        df.online = False
        df.save()
        df = DataFile.objects.create(dataset=ds, **self.second_file_params)
        df.online = False
        df.save()
        self.assertEqual(ds.online_status, "offline")

    def test_string_version(self):
        ds = DataSet.objects.create(name="OBS", version="1")
        self.assertEqual(str(ds), "OBS (1)")

    def test_string_no_version(self):
        ds = DataSet.objects.create(name="OBS", version=None)
        self.assertEqual(str(ds), "OBS")


# TODO when more attributes have been added to the DataFile model then add tests
class TestDataFile(TestCase):
    """Test the DataFile object"""

    def setUp(self):
        self.ds = DataSet.objects.create(name="OBS", version="1")
        self.basic_file_params = {
            "name": "obs_day_OBS-1_1deg_197801_201812.nc",
            "incoming_directory": "/some/dir",
            "directory": "/some/dir",
            "online": True,
            "size": 1,
        }

    # def test_variable_standard_name(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          standard_name='cloud_albedo',
    #                                          long_name='wibble wobble',
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertEqual(df.variable, 'cloud_albedo')
    #
    # def test_variable_long_name(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          long_name='wibble wobble',
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertEqual(df.variable, 'wibble wobble')
    #
    # def test_variable_var_name(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          var_name='wobble wabble',
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertEqual(df.variable, 'wobble wabble')
    #
    # def test_variable_not_specified(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertIsNone(df.variable)
    #
    # def test_start_string_none(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertIsNone(df.start_string)
    #
    # def test_start_string_zero(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          start_time=0.0,
    #                                          calendar='gregorian',
    #                                          time_units='days since 1950-01-01',
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertEqual(df.start_string, '1950-01-01')
    #
    # def test_start_string(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          start_time=364.99,
    #                                          calendar='gregorian',
    #                                          time_units='days since 1950-01-01',
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertEqual(df.start_string, '1950-12-31')
    #
    # def test_end_string_none(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertIsNone(df.end_string)
    #
    # def test_end_string_zero(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          end_time=0.0,
    #                                          calendar='gregorian',
    #                                          time_units='days since 1950-01-01',
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertEqual(df.end_string, '1950-01-01')
    #
    # def test_end_string(self):
    #     df = DataFile.objects.create(dataset=self.ds,
    #                                          end_time=181.5,
    #                                          calendar='gregorian',
    #                                          time_units='days since 1950-01-01',
    #                                          **self.basic_file_params)
    #     df.save()
    #     self.assertEqual(df.end_string, '1950-07-01')

    def test_string(self):
        df = DataFile.objects.create(dataset=self.ds, **self.basic_file_params)
        df.save()
        self.assertEqual(
            str(df), "obs_day_OBS-1_1deg_197801_201812.nc (Directory: /some/dir)"
        )
