"""
Test dmt_app.utils.common
"""
from unittest import mock

from django.test import TestCase

from dmt_app.utils.common import adler32, md5, sha256


class TestChecksums(TestCase):
    """ Test dmt_app.utils.common.sha256(), md5() and adler32() """
    def setUp(self):
        patch = mock.patch('dmt_app.utils.common.subprocess.run')
        self.mock_run = patch.start()
        self.addCleanup(patch.stop)

    def test_adler32_success(self):
        class CompletedProcess:
            returncode = 0
            stdout = '0123456789 /some/path'
        self.mock_run.return_value = CompletedProcess
        self.assertEqual(adler32('/some/path'), '0123456789')

    def test_adler32_fails(self):
        class CompletedProcess:
            returncode = 1
            stdout = ''
            stderr = 'Error message'
        self.mock_run.return_value = CompletedProcess
        self.assertEqual(adler32('/some/path'), None)

    def test_md5_success(self):
        class CompletedProcess:
            returncode = 0
            stdout = 'abcdef0123456789 /some/path'
        self.mock_run.return_value = CompletedProcess
        self.assertEqual(md5('/some/path'), 'abcdef0123456789')

    def test_md5_fails(self):
        class CompletedProcess:
            returncode = 1
            stdout = ''
            stderr = 'Error message'
        self.mock_run.return_value = CompletedProcess
        self.assertEqual(md5('/some/path'), None)

    def test_sha256_success(self):
        class CompletedProcess:
            returncode = 0
            stdout = '0123456789abcdef /some/path'
        self.mock_run.return_value = CompletedProcess
        self.assertEqual(sha256('/some/path'), '0123456789abcdef')

    def test_sha256_fails(self):
        class CompletedProcess:
            returncode = 1
            stdout = ''
            stderr = 'Error message'
        self.mock_run.return_value = CompletedProcess
        self.assertEqual(sha256('/some/path'), None)
