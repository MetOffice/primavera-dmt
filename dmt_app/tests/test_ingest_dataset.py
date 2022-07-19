# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

# pylint: disable=missing-function-docstring

"""
test_ingest_dataset.py

Unit tests for bin/ingest_dataset.py the CLI software in add datasets to the DMT
"""
import ast
import os
import stat
import tempfile
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import RequestsClient

from dmt_app.models import DataFile
from dmt_app.utils.ingestion import (
    CredentialsFileError,
    DmtCredentials,
    IngestedDataset,
)
from .test_utils.common import make_sample_netcdf


class TestDmtCredentials(TestCase):
    """Test dmt_app.utils.ingestion.DmtCredentials"""

    def setUp(self):
        _fd, self.creds_filename = tempfile.mkstemp(suffix=".json")
        self.creds_text = """{
    "url": "http://localhost:8000/api/",
    "username": "joebloggs",
    "password": "h!wkp#_ia%a%"
}"""
        with open(self.creds_filename, "w", encoding="utf-8") as hndl:
            hndl.write(self.creds_text)
        # Set permissions to 0o400 (r--------)
        os.chmod(self.creds_filename, stat.S_IRUSR)

    def tearDown(self):
        try:
            os.remove(self.creds_filename)
        except FileNotFoundError:
            pass

    def test_load(self):
        creds = DmtCredentials(self.creds_filename)
        # pylint: disable=protected-access
        self.assertEqual(creds._json, ast.literal_eval(self.creds_text))

    def test_permissions_user_write(self):
        os.chmod(self.creds_filename, stat.S_IRUSR | stat.S_IWUSR)
        self.assertRaisesRegex(
            CredentialsFileError,
            "has permissions 600 but must be 400",
            DmtCredentials,
            self.creds_filename,
        )

    def test_not_exist(self):
        os.remove(self.creds_filename)
        self.assertRaisesRegex(
            CredentialsFileError,
            f"Credentials file {self.creds_filename} does not exist.",
            DmtCredentials,
            self.creds_filename,
        )

    def test_symlink(self):
        _fd, symlink_filename = tempfile.mkstemp(suffix=".json")
        # mkstemp() creates a file so remove this so that the symlink can be created
        os.remove(symlink_filename)
        os.symlink(self.creds_filename, symlink_filename)
        self.assertRaisesRegex(
            CredentialsFileError,
            f"Credentials file {symlink_filename} is a symbolic link.",
            DmtCredentials,
            symlink_filename,
        )
        os.remove(symlink_filename)

    def test_url(self):
        creds = DmtCredentials(self.creds_filename)
        self.assertEqual(creds.url, "http://localhost:8000/api/")

    def test_username(self):
        creds = DmtCredentials(self.creds_filename)
        self.assertEqual(creds.username, "joebloggs")

    def test_password(self):
        creds = DmtCredentials(self.creds_filename)
        self.assertEqual(creds.password, "h!wkp#_ia%a%")


class TestIngestion(TestCase):
    """Integration test for dmt_app.utils.ingestion.IngestedDataset"""

    def setUp(self):
        """Create sample files"""
        self.dataset_dir = tempfile.mkdtemp()
        _fd, self.netcdf_filename = tempfile.mkstemp(suffix=".nc", dir=self.dataset_dir)
        make_sample_netcdf(self.netcdf_filename)
        _fd, self.text_filename = tempfile.mkstemp(suffix=".txt", dir=self.dataset_dir)
        # Create a user so that the API can be used
        self.test_user_attributes = {
            "username": "joebloggs",
            "email": "test@test.com",
            "password": "h!wkp#_ia%a%",
        }
        get_user_model().objects.create_user(**self.test_user_attributes)
        # Use mock to monkey patch in the test client
        self.client = RequestsClient()
        patch = mock.patch("dmt_app.utils.ingestion.requests.post")
        self.requests_post = patch.start()
        self.requests_post.side_effect = self.client.post
        self.addCleanup(patch.stop)
        patch = mock.patch("dmt_app.utils.ingestion.requests.get")
        self.requests_post = patch.start()
        self.requests_post.side_effect = self.client.get
        self.addCleanup(patch.stop)

    def test_ingestion_netcdf_only(self):
        dataset = IngestedDataset("DATASET", "V1.0", self.dataset_dir)
        dataset.add_files(only_netcdf=True)
        dataset.to_django_instance(
            "http://testserver/api/",
            self.test_user_attributes["username"],
            self.test_user_attributes["password"],
        )
        self.assertEqual(DataFile.objects.count(), 1)
        data_file = DataFile.objects.get(name=os.path.basename(self.netcdf_filename))
        self.assertEqual(data_file.incoming_directory, self.dataset_dir)
        self.assertEqual(data_file.directory, self.dataset_dir)
        file_size = os.stat(
            os.path.join(self.dataset_dir, self.netcdf_filename)
        ).st_size
        self.assertEqual(data_file.size, file_size)
        self.assertTrue(data_file.online)
        self.assertEqual(data_file.dataset.name, "DATASET")
        self.assertEqual(data_file.dataset.version, "V1.0")
        self.assertEqual(data_file.start_string, "2014-12-21")
        self.assertEqual(data_file.end_string, "2014-12-24")
        self.assertEqual(
            data_file.standard_name,
            "sea_water_salinity, air_temperature, sea_surface_temperature",
        )
        self.assertEqual(data_file.var_name, "so, tas, tos")
        self.assertEqual(
            data_file.long_name,
            "Sea Water Salinity, Near-Surface Air Temperature",
        )
        self.assertEqual(data_file.units, "0.001, K")
        self.assertIsNone(data_file.frequency)
        self.assertEqual(data_file.dimensions, "time, grid_latitude, grid_longitude")

    def test_ingestion_all_file_types(self):
        dataset = IngestedDataset("DATASET", "V1.0", self.dataset_dir)
        dataset.add_files(only_netcdf=False)
        dataset.to_django_instance(
            "http://testserver/api/",
            self.test_user_attributes["username"],
            self.test_user_attributes["password"],
        )
        self.assertEqual(DataFile.objects.count(), 2)
        # Check netCDF file
        data_file = DataFile.objects.get(name=os.path.basename(self.netcdf_filename))
        self.assertEqual(data_file.incoming_directory, self.dataset_dir)
        self.assertEqual(data_file.directory, self.dataset_dir)
        file_size = os.stat(
            os.path.join(self.dataset_dir, self.netcdf_filename)
        ).st_size
        self.assertEqual(data_file.size, file_size)
        self.assertTrue(data_file.online)
        self.assertEqual(data_file.dataset.name, "DATASET")
        self.assertEqual(data_file.dataset.version, "V1.0")
        self.assertEqual(data_file.start_string, "2014-12-21")
        self.assertEqual(data_file.end_string, "2014-12-24")
        self.assertEqual(
            data_file.standard_name,
            "sea_water_salinity, air_temperature, sea_surface_temperature",
        )
        self.assertEqual(data_file.var_name, "so, tas, tos")
        self.assertEqual(
            data_file.long_name,
            "Sea Water Salinity, Near-Surface Air Temperature",
        )
        self.assertEqual(data_file.units, "0.001, K")
        self.assertIsNone(data_file.frequency)
        self.assertEqual(data_file.dimensions, "time, grid_latitude, grid_longitude")
        # Check text file
        data_file = DataFile.objects.get(name=os.path.basename(self.text_filename))
        self.assertEqual(data_file.incoming_directory, self.dataset_dir)
        self.assertEqual(data_file.directory, self.dataset_dir)
        file_size = os.stat(os.path.join(self.dataset_dir, self.text_filename)).st_size
        self.assertEqual(data_file.size, file_size)
        self.assertTrue(data_file.online)
        self.assertEqual(data_file.dataset.name, "DATASET")
        self.assertEqual(data_file.dataset.version, "V1.0")

    def tearDown(self) -> None:
        """Remove temporary files"""
        os.remove(self.netcdf_filename)
        os.remove(self.text_filename)
        os.rmdir(self.dataset_dir)
