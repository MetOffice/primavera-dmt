# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

# pylint: disable=missing-function-docstring, missing-class-docstring
# pylint: disable=too-few-public-methods

"""
Test dmt_app.utils.common
"""
from pathlib import Path
import shutil
import tempfile
from unittest import mock

from django.test import TestCase

from dmt_app.utils.common import adler32, list_files, md5, sha256


class BasePathIteratorTest(TestCase):
    """
    An base class for tests that involve iterating through a directory
    structure.
    """

    def setUp(self):
        """
        Create a temporary file structure with the structure:
        .
        |-- dir1
        |   |-- dir2
        |   |   `-- dir3
        |   `-- file3.nc
        |   `-- file4.nc -> file3.nc
        |   `-- file5.pp
        |-- file1.nc
        `-- file2.pp
        """
        temp_path = tempfile.mkdtemp()
        temp_dir = Path(temp_path)
        dir1 = temp_dir.joinpath("dir1")
        dir1.mkdir()
        temp_dir.joinpath("file1.nc").touch()
        temp_dir.joinpath("file2.pp").touch()
        dir2 = dir1.joinpath("dir2")
        dir2.mkdir()
        file3 = dir1.joinpath("file3.nc")
        file3.touch()
        dir1.joinpath("file4.nc").symlink_to(file3)
        dir1.joinpath("file5.pp").touch()
        dir2.joinpath("dir3").mkdir()
        self.temp_dir = temp_dir

    def tearDown(self):
        """
        Remove the temporary file structure
        """
        shutil.rmtree(self.temp_dir)


class TestListFiles(BasePathIteratorTest):
    """
    Test list_files
    """

    def test_list_files_default_suffix(self):
        actual_tree_list = list_files(self.temp_dir)
        expected_files = ["file1.nc", "dir1/file3.nc", "dir1/file4.nc"]
        expected_tree_list = [
            self.temp_dir.joinpath(ef).as_posix() for ef in expected_files
        ]
        actual_tree_list.sort()
        expected_tree_list.sort()
        self.assertEqual(actual_tree_list, expected_tree_list)

    def test_list_files_any_suffix(self):
        actual_tree_list = list_files(self.temp_dir, suffix="")
        expected_files = [
            "file1.nc",
            "file2.pp",
            "dir1/file3.nc",
            "dir1/file4.nc",
            "dir1/file5.pp",
        ]
        expected_tree_list = [
            self.temp_dir.joinpath(ef).as_posix() for ef in expected_files
        ]
        actual_tree_list.sort()
        expected_tree_list.sort()
        self.assertEqual(actual_tree_list, expected_tree_list)


class TestChecksums(TestCase):
    """Test dmt_app.utils.common.sha256(), md5() and adler32()"""

    def setUp(self):
        patch = mock.patch("dmt_app.utils.common.subprocess.run")
        self.mock_run = patch.start()
        self.addCleanup(patch.stop)

    def test_adler32_success(self):
        class CompletedProcess:
            returncode = 0
            stdout = b"0123456789 /some/path"

        self.mock_run.return_value = CompletedProcess
        self.assertEqual(adler32("/some/path"), "0123456789")

    def test_adler32_fails(self):
        class CompletedProcess:
            returncode = 1
            stdout = b""

        self.mock_run.return_value = CompletedProcess
        self.assertEqual(adler32("/some/path"), None)

    def test_md5_success(self):
        class CompletedProcess:
            returncode = 0
            stdout = b"abcdef0123456789 /some/path"

        self.mock_run.return_value = CompletedProcess
        self.assertEqual(md5("/some/path"), "abcdef0123456789")

    def test_md5_fails(self):
        class CompletedProcess:
            returncode = 1
            stdout = b""

        self.mock_run.return_value = CompletedProcess
        self.assertEqual(md5("/some/path"), None)

    def test_sha256_success(self):
        class CompletedProcess:
            returncode = 0
            stdout = b"0123456789abcdef /some/path"

        self.mock_run.return_value = CompletedProcess
        self.assertEqual(sha256("/some/path"), "0123456789abcdef")

    def test_sha256_fails(self):
        class CompletedProcess:
            returncode = 1
            stdout = b""

        self.mock_run.return_value = CompletedProcess
        self.assertEqual(sha256("/some/path"), None)
