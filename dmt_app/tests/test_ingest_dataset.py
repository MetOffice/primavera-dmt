# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
test_ingest_dataset.py

Unit tests for bin/ingest_dataset.py the CLI software in add datasets to the DMT
"""
import os
import stat
import tempfile

from django.test import TestCase

from dmt_app.utils.ingestion import CredentialsFileError, DmtCredentials


class TestDmtCredentials(TestCase):
    """Test dmt_app.utils.ingestion.DmtCredentials"""
    def setUp(self):
        _fd, self.creds_filename = tempfile.mkstemp(suffix='.json')
        self.creds_text = """{
    "url": "http://localhost:8000/api/",
    "username": "joebloggs",
    "password": "h!wkp#_ia%a%"
}"""
        with open(self.creds_filename, 'w') as fh:
            fh.write(self.creds_text)
        # Set permissions to 0o400 (r--------)
        os.chmod(self.creds_filename, stat.S_IRUSR)

    def tearDown(self):
        try:
            os.remove(self.creds_filename)
        except FileNotFoundError:
            pass

    def test_load(self):
        creds = DmtCredentials(self.creds_filename)
        self.assertEqual(creds._json, eval(self.creds_text))

    def test_permissions_user_write(self):
        os.chmod(self.creds_filename, stat.S_IRUSR | stat.S_IWUSR)
        self.assertRaisesRegex(CredentialsFileError,
                                'has permissions 600 but must be 400', DmtCredentials,
                                self.creds_filename)

    def test_not_exist(self):
        os.remove(self.creds_filename)
        self.assertRaisesRegex(CredentialsFileError,
                                f'Credentials file {self.creds_filename} does not '
                                f'exist.', DmtCredentials, self.creds_filename)

    def test_symlink(self):
        _fd, symlink_filename = tempfile.mkstemp(suffix='.json')
        # mkstemp() creates a file so remove this so that the symlink can be created
        os.remove(symlink_filename)
        os.symlink(self.creds_filename, symlink_filename)
        self.assertRaisesRegex(CredentialsFileError,
                                f'Credentials file {symlink_filename} is a '
                                f'symbolic link.', DmtCredentials, symlink_filename)
        os.remove(symlink_filename)

    def test_url(self):
        creds = DmtCredentials(self.creds_filename)
        self.assertEqual(creds.url, 'http://localhost:8000/api/')

    def test_username(self):
        creds = DmtCredentials(self.creds_filename)
        self.assertEqual(creds.username, 'joebloggs')

    def test_password(self):
        creds = DmtCredentials(self.creds_filename)
        self.assertEqual(creds.password, 'h!wkp#_ia%a%')
