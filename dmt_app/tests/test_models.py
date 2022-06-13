# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

# pylint: disable=missing-function-docstring

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
        data_set = DataSet.objects.create(name="OBS", version="1")
        self.assertEqual(data_set.name, "OBS")
        self.assertEqual(data_set.version, "1")

    def test_add_file(self):
        data_set = DataSet.objects.create(name="OBS", version="1")
        data_file = DataFile.objects.create(dataset=data_set, **self.first_file_params)
        data_file.save()
        self.assertEqual(data_set.datafile_set.count(), 1)

    def test_status_online(self):
        data_set = DataSet.objects.create(name="OBS", version="1")
        data_file = DataFile.objects.create(dataset=data_set, **self.first_file_params)
        data_file.save()
        data_file = DataFile.objects.create(dataset=data_set, **self.second_file_params)
        data_file.save()
        self.assertEqual(data_set.online_status, "online")

    def test_status_partial(self):
        data_set = DataSet.objects.create(name="OBS", version="1")
        data_file = DataFile.objects.create(dataset=data_set, **self.first_file_params)
        data_file.save()
        data_file = DataFile.objects.create(dataset=data_set, **self.second_file_params)
        data_file.online = False
        data_file.save()
        self.assertEqual(data_set.online_status, "partial")

    def test_status_offline(self):
        data_set = DataSet.objects.create(name="OBS", version="1")
        data_file = DataFile.objects.create(dataset=data_set, **self.first_file_params)
        data_file.online = False
        data_file.save()
        data_file = DataFile.objects.create(dataset=data_set, **self.second_file_params)
        data_file.online = False
        data_file.save()
        self.assertEqual(data_set.online_status, "offline")

    def test_string_version(self):
        data_set = DataSet.objects.create(name="OBS", version="1")
        self.assertEqual(str(data_set), "OBS (1)")

    def test_string_no_version(self):
        data_set = DataSet.objects.create(name="OBS", version=None)
        self.assertEqual(str(data_set), "OBS")


# TODO when more attributes have been added to the DataFile model then add tests
class TestDataFile(TestCase):
    """Test the DataFile object"""

    def setUp(self):
        self.data_set = DataSet.objects.create(name="OBS", version="1")
        self.basic_file_params = {
            "name": "obs_day_OBS-1_1deg_197801_201812.nc",
            "incoming_directory": "/some/dir",
            "directory": "/some/dir",
            "online": True,
            "size": 1,
        }

    # def test_variable_standard_name(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          standard_name='cloud_albedo',
    #                                          long_name='wibble wobble',
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertEqual(data_file.variable, 'cloud_albedo')
    #
    # def test_variable_long_name(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          long_name='wibble wobble',
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertEqual(data_file.variable, 'wibble wobble')
    #
    # def test_variable_var_name(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          var_name='wobble wabble',
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertEqual(data_file.variable, 'wobble wabble')
    #
    # def test_variable_not_specified(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertIsNone(data_file.variable)
    #
    # def test_start_string_none(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertIsNone(data_file.start_string)
    #
    # def test_start_string_zero(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          start_time=0.0,
    #                                          calendar='gregorian',
    #                                          time_units='days since 1950-01-01',
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertEqual(data_file.start_string, '1950-01-01')
    #
    # def test_start_string(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          start_time=364.99,
    #                                          calendar='gregorian',
    #                                          time_units='days since 1950-01-01',
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertEqual(data_file.start_string, '1950-12-31')
    #
    # def test_end_string_none(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertIsNone(data_file.end_string)
    #
    # def test_end_string_zero(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          end_time=0.0,
    #                                          calendar='gregorian',
    #                                          time_units='days since 1950-01-01',
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertEqual(data_file.end_string, '1950-01-01')
    #
    # def test_end_string(self):
    #     data_file = DataFile.objects.create(dataset=self.data_set,
    #                                          end_time=181.5,
    #                                          calendar='gregorian',
    #                                          time_units='days since 1950-01-01',
    #                                          **self.basic_file_params)
    #     data_file.save()
    #     self.assertEqual(data_file.end_string, '1950-07-01')

    def test_string(self):
        data_file = DataFile.objects.create(
            dataset=self.data_set, **self.basic_file_params
        )
        data_file.save()
        self.assertEqual(
            str(data_file), "obs_day_OBS-1_1deg_197801_201812.nc (Directory: /some/dir)"
        )
