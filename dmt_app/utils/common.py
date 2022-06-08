# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
Common functions used throughout the project.
"""
import os
import subprocess


def list_files(directory, suffix='.nc'):
    """
    Return a list of all the files with the specified suffix in the submission
    directory structure and subdirectories.

    :param str directory: The root directory of the submission
    :param str suffix: The suffix of the files of interest
    :returns: A list of absolute filepaths
    :rtype: list
    """
    # TODO rewrite using Path objects
    nc_files = []

    dir_files = os.listdir(directory)
    for filename in dir_files:
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            nc_files.extend(list_files(file_path, suffix))
        elif file_path.endswith(suffix):
            nc_files.append(file_path)

    return nc_files


def adler32(fpath):
    return _checksum('adler32', fpath)


def md5(fpath):
    return _checksum('md5sum', fpath)


def sha256(fpath):
    return _checksum('sha256sum', fpath)


def _checksum(checksum_method, file_path):
    """
    Runs program `checksum_method` on `file_path` and returns the result or
    None if running the program was unsuccessful.

    :param str checksum_method: The name of the checksum executable to run
    :param str file_path: The full path of teh file to check
    :returns: the checksum or None if it cannot be calculated
    :rtype: str
    """
    command = f"{checksum_method} '{file_path}'"
    completed = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    if completed.returncode != 0:
        checksum = None
    else:
        checksum = completed.stdout.decode('UTF-8').split()[0]

    return checksum
