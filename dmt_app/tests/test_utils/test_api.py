# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

# pylint: disable=missing-function-docstring

"""
Test the API

This is done using the RequestsClient, which is the interface that other programs
interacting with the API will see. There are alternative lower level rest_framework
options to test just the serializer, but this almost integration test seemed
preferable to guarantee the correct testing of user interactions.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
import requests
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient

from dmt_app.models import DataFile, DataSet
from .common import SampleDjangoEntities


class TestBasicGetApi(TestCase):
    """Basic API test to read data"""

    def setUp(self):
        """Create dummy data in database"""
        self.sample_data = SampleDjangoEntities().make_django_entities()
        self.client = RequestsClient()
        self.base_url = "http://testserver/api/"
        # See an unlimited diff in case of error
        self.maxDiff = None  # pylint: disable=invalid-name

    def test_specified_dataset_returned(self):
        response = self.client.get(
            f"{self.base_url}datasets/{self.sample_data.dataset.id}/"
        )
        # pylint: disable=no-member
        self.assertEqual(response.status_code, requests.codes.ok)
        expected = {
            "id": self.sample_data.dataset.id,
            "name": self.sample_data.dataset.name,
            "version": self.sample_data.dataset.version,
            "url": None,
            "summary": None,
            "doi": None,
            "reference": None,
            "license": None,
            "date_downloaded": None,
            "datafile_set": [
                f"{self.base_url}datafiles/{self.sample_data.datafile1.id}/",
                f"{self.base_url}datafiles/{self.sample_data.datafile2.id}/",
            ],
        }
        self.assertEqual(response.json(), expected)

    def test_all_datasets_returned(self):
        response = self.client.get(f"{self.base_url}datasets/")
        # pylint: disable=no-member
        self.assertEqual(response.status_code, requests.codes.ok)
        expected = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.sample_data.dataset.id,
                    "name": self.sample_data.dataset.name,
                    "version": self.sample_data.dataset.version,
                    "url": None,
                    "summary": None,
                    "doi": None,
                    "reference": None,
                    "license": None,
                    "date_downloaded": None,
                    "datafile_set": [
                        f"{self.base_url}datafiles/{self.sample_data.datafile1.id}/",
                        f"{self.base_url}datafiles/{self.sample_data.datafile2.id}/",
                    ],
                }
            ],
        }
        self.assertEqual(response.json(), expected)

    def test_specified_datafile_returned(self):
        response = self.client.get(
            f"{self.base_url}datafiles/{self.sample_data.datafile2.id}/"
        )
        # pylint: disable=no-member
        self.assertEqual(response.status_code, requests.codes.ok)
        expected = {
            "id": self.sample_data.datafile2.id,
            "name": self.sample_data.datafile2.name,
            "incoming_directory": self.sample_data.datafile2.incoming_directory,
            "directory": None,
            "size": self.sample_data.datafile2.size,
            "checksum_value": self.sample_data.datafile2.checksum_value,
            "checksum_type": self.sample_data.datafile2.checksum_type,
            "online": self.sample_data.datafile2.online,
            "time_units": None,
            "calendar": None,
            "start_time": None,
            "end_time": None,
            "frequency": None,
            "standard_name": None,
            "long_name": None,
            "var_name": None,
            "units": None,
            "dimensions": None,
            "dataset": f"{self.base_url}datasets/{self.sample_data.dataset.id}/",
        }
        self.assertEqual(response.json(), expected)

    def test_all_datafiles_returned(self):
        response = self.client.get(f"{self.base_url}datafiles/")
        # pylint: disable=no-member
        self.assertEqual(response.status_code, requests.codes.ok)
        expected = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.sample_data.datafile1.id,
                    "name": self.sample_data.datafile1.name,
                    "incoming_directory": self.sample_data.datafile1.incoming_directory,
                    "directory": None,
                    "size": self.sample_data.datafile1.size,
                    "checksum_value": self.sample_data.datafile1.checksum_value,
                    "checksum_type": self.sample_data.datafile1.checksum_type,
                    "online": self.sample_data.datafile1.online,
                    "time_units": None,
                    "calendar": None,
                    "start_time": None,
                    "end_time": None,
                    "frequency": None,
                    "standard_name": None,
                    "long_name": None,
                    "var_name": None,
                    "units": None,
                    "dimensions": None,
                    "dataset": (
                        f"{self.base_url}datasets/{self.sample_data.dataset.id}/"
                    ),
                },
                {
                    "id": self.sample_data.datafile2.id,
                    "name": self.sample_data.datafile2.name,
                    "incoming_directory": self.sample_data.datafile2.incoming_directory,
                    "directory": None,
                    "size": self.sample_data.datafile2.size,
                    "checksum_value": self.sample_data.datafile2.checksum_value,
                    "checksum_type": self.sample_data.datafile2.checksum_type,
                    "online": self.sample_data.datafile2.online,
                    "time_units": None,
                    "calendar": None,
                    "start_time": None,
                    "end_time": None,
                    "frequency": None,
                    "standard_name": None,
                    "long_name": None,
                    "var_name": None,
                    "units": None,
                    "dimensions": None,
                    "dataset": (
                        f"{self.base_url}datasets/{self.sample_data.dataset.id}/"
                    ),
                },
            ],
        }
        self.assertEqual(response.json(), expected)


class TestBasicPostApi(TestCase):
    """Basic API test to add data"""

    def setUp(self):
        """Set-up common to all put tests"""
        # User with write permissions set-up
        self.test_user_attributes = {
            "username": "test1",
            "email": "test@test.com",
            "password": "qwe123qwe",
        }
        get_user_model().objects.create_user(**self.test_user_attributes)
        # Client set-up
        self.client = RequestsClient()
        self.base_url = "http://testserver/api/"
        self.client.auth = HTTPBasicAuth(
            self.test_user_attributes["username"],
            self.test_user_attributes["password"],
        )
        self.client.headers.update({"x-test": "true"})
        # Sample data
        self.sample_data = SampleDjangoEntities()
        # See an unlimited diff in case of error
        self.maxDiff = None  # pylint: disable=invalid-name

    def test_create_dataset(self):
        self.sample_data.dataset_attrs["datafile_set"] = []
        response = self.client.post(
            f"{self.base_url}datasets/",
            json=self.sample_data.dataset_attrs,
        )
        # Check that the set was created successfully
        # pylint: disable=no-member
        self.assertEqual(response.status_code, requests.codes.created)
        dataset = DataSet.objects.get(
            name=self.sample_data.dataset_attrs["name"],
            version=self.sample_data.dataset_attrs["version"],
        )
        # Check that the creator attribute in the API response matches that in the DB
        self.assertEqual(dataset.creator, self.test_user_attributes["username"])

    def test_create_datafile(self):
        # Have to create a set first
        self.sample_data.dataset_attrs["datafile_set"] = []
        dataset_response = self.client.post(
            f"{self.base_url}datasets/",
            json=self.sample_data.dataset_attrs,
        )
        # pylint: disable=no-member
        self.assertEqual(dataset_response.status_code, requests.codes.created)
        dataset_id = dataset_response.json()["id"]
        dataset_url = f"{self.base_url}datasets/{dataset_id}/"
        # Can now create and test a DataFile
        self.sample_data.datafile1_attrs["dataset"] = dataset_url
        datafile_response = self.client.post(
            f"{self.base_url}datafiles/",
            json=self.sample_data.datafile1_attrs,
        )
        # Check that the file was created successfully
        # pylint: disable=no-member
        self.assertEqual(datafile_response.status_code, requests.codes.created)
        datafile = DataFile.objects.get(
            name=self.sample_data.datafile1_attrs["name"],
            incoming_directory=self.sample_data.datafile1_attrs["incoming_directory"],
        )
        # Check that all compulsory attributes were created successfully
        for key, value in self.sample_data.datafile1_attrs.items():
            if key == "dataset":
                self.assertEqual(datafile.dataset.id, dataset_id)
            else:
                self.assertEqual(getattr(datafile, key), value)
