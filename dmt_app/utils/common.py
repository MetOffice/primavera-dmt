"""
Common functions used throughout the project.
"""
import os
from subprocess import check_output, CalledProcessError



def list_files(directory, suffix='.nc'):
    """
    Return a list of all the files with the specified suffix in the submission
    directory structure and sub-directories.

    :param str directory: The root directory of the submission
    :param str suffix: The suffix of the files of interest
    :returns: A list of absolute filepaths
    """
    nc_files = []

    dir_files = os.listdir(directory)
    for filename in dir_files:
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            nc_files.extend(list_files(file_path, suffix))
        elif file_path.endswith(suffix):
            nc_files.append(file_path)

    return nc_files


def md5(fpath):
    return _checksum('md5sum', fpath)


def sha256(fpath):
    return _checksum('sha256sum', fpath)


def adler32(fpath):
    return _checksum('adler32', fpath)


def _checksum(checksum_method, file_path):
    """
    Runs program `checksum_method` on `file_path` and returns the result or
    None if running the program was unsuccessful.

    :param str command:
    :param str file_path:
    :return: the checksum or None if it cannot be calculated
    """
    try:
        # shell=True is not a security risk here. The input has previously been
        # checked and this is only called if file_path has been confirmed as
        # being a valid file
        # TODO convert to subprocess.run
        ret_val = check_output("{} '{}'".format(checksum_method, file_path),
                                shell=True).decode('utf-8')
        # split on white space and return the first part
        checksum = ret_val.split()[0]
    except (CalledProcessError, OSError):
        checksum = None

    return checksum
