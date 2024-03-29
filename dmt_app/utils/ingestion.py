# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

# pylint: disable=missing-class-docstring

"""
Various classes to ingest datasets into the DMT
"""
from http.client import responses
import json
import logging
import os
from pathlib import Path

from netCDF4 import Dataset  # pylint: disable=no-name-in-module
import requests

from dmt_app.utils.common import list_files, sha256

logger = logging.getLogger(__name__)


class APIQueryError(Exception):
    def __init__(self, message, server_message=None):
        """
        A custom exception for when an API query fails.

        :param str message: Default exception message.
        :param str server_message: The error message returned from the server.
        """
        super().__init__(message)
        self.server_message = server_message


class CredentialsFileError(Exception):
    """
    Custom exception raised when there is a problem with a user's credentials file.
    """


class DmtCredentials:
    def __init__(self, settings_file):
        """
        Represent, check and access a user's credentials from their settings file. The
        file must be a regular file with Unix permissions 400 (read-only to the user).

        :param str settings_file: The path to the settings file.
        """
        self.path = Path(settings_file).expanduser()
        self._check_credentials()
        with open(self.path, encoding="utf-8") as hndl:
            self._json = json.load(hndl)

    @property
    def url(self):
        """Return the URL from the file"""
        return self._json["url"]

    @property
    def username(self):
        """Return the username from the file"""
        return self._json["username"]

    @property
    def password(self):
        """Return the password from the file"""
        return self._json["password"]

    def _check_credentials(self):
        """
        Check that the credentials file exists and are protected.

        :raises CredentialsFileError: When there is a problem with a user's
            credentials file.
        """
        if not self.path.exists():
            raise CredentialsFileError(f"Credentials file {self.path} does not exist.")
        if self.path.is_symlink():
            raise CredentialsFileError(
                f"Credentials file {self.path} is a symbolic link."
            )
        if not self.path.is_file():
            raise CredentialsFileError(f"Credentials file {self.path} is not a file.")

        mask_3_bytes = 0o777
        permissions_bytes = self.path.stat().st_mode & mask_3_bytes
        user_read_only = 0o400
        if not permissions_bytes == user_read_only:
            msg = (
                f"Credentials file {self.path} has permissions "
                f"{oct(permissions_bytes)[-3:]} but must be "
                f"{oct(user_read_only)[-3:]}"
            )
            raise CredentialsFileError(msg)


class IngestedDataset:
    """
    An ingested data set that can have files added to it and can then be added
    to the database.
    """

    # The attributes that are required in the class to fully describe a
    # data set
    django_attributes = ["name", "version"]

    def __init__(self, name=None, version=None, incoming_directory=None):
        """
        Create a new data set.

        :param str name: The name of the set.
        :param str version: The set's version
        :param str incoming_directory: The local path that the set is
            stored at.
        :raises ValueError: if the path specified is not a valid directory.
        """
        if not os.path.exists(incoming_directory):
            msg = f"Directory does not exist: {incoming_directory}"
            raise ValueError(msg)

        if not os.path.isdir(incoming_directory):
            msg = f"Path is not a directory: {incoming_directory}"
            raise ValueError(msg)

        self.name = name
        self.version = version
        # The related observation files
        self.datafiles = []
        # This isn't needed for Django, but is convenient to hold in this class
        self.incoming_directory = incoming_directory

    def add_files(self, only_netcdf=False):
        """
        Identify any files in the incoming directory and its subdirectories.
        Obtain all relevant metadata from each of the files found. There
        is also the option to ignore any files without a .nc suffix.

        :raises ValueError: if no files were found.
        """
        if only_netcdf:
            # TODO replace with ilist_files
            found_files = list_files(self.incoming_directory)
        else:
            found_files = list_files(self.incoming_directory, "")

        if not found_files:
            msg = (
                f"No files found in directory or its subdirectories "
                f"{self.incoming_directory}"
            )
            raise ValueError(msg)

        logger.debug(f"{len(found_files)} files identified")

        for found_file in found_files:
            data_file = IngestedDatafile(
                os.path.basename(found_file), os.path.dirname(found_file)
            )
            data_file.add_metadata()
            self.datafiles.append(data_file)

        logger.debug(f"{len(self.datafiles)} files added")

    def to_django_instance(self, base_url, username, password):
        """
        Convert this object into a Django dmt_app.models.DataSet
        instance of the same observations set. Instances of each file in the
        set are also created.

        :param str base_url: The URL of the root of the API on the server ending with
            a forward slash.
        :param str password: The password to use in the API call.
        :param str username: The username to use in the API call.
        """
        # Post the new dataset to the server
        json_attributes = {"datafile_set": []}
        for attr in self.django_attributes:
            json_attributes[attr] = getattr(self, attr)

        url = f"{base_url}datasets/"
        response = requests.post(
            url, json=json_attributes, auth=(username, password), timeout=5.0
        )
        if response.status_code != requests.codes.created:  # pylint: disable=no-member
            msg = (
                f"{response.status_code} ({responses[response.status_code]}) "
                f"response from HTTP POST {response.url} {self.name} "
                f"{self.version}"
            )
            raise APIQueryError(msg, server_message=response.text)

        # Get the URL of dataset in the API
        query_params = {attr: getattr(self, attr) for attr in self.django_attributes}
        request = requests.get(f"{base_url}datasets/", params=query_params, timeout=5.0)
        if request.status_code != requests.codes.ok:  # pylint: disable=no-member
            msg = (
                f"{request.status_code} ({responses[request.status_code]}) "
                f"response from HTTP GET {request.url}"
            )
            raise APIQueryError(msg, server_message=response.text)
        query_json = request.json()
        num_results = len(query_json["results"])
        if num_results == 0:  # pylint: disable=no-else-raise
            raise APIQueryError(
                f"No datasets found, expecting one from HTTP GET {request.url}"
            )
        elif num_results > 1:
            raise APIQueryError(
                f"{num_results} datasets found, expecting one "
                f"from HTTP GET {request.url}"
            )
        else:
            dataset_url = f'{base_url}datasets/{query_json["results"][0]["id"]}/'

        # Add the files to dataset
        for datafile_obj in self.datafiles:
            datafile_obj.to_django_instance(base_url, dataset_url, username, password)


class IngestedDatafile:
    """
    A class that represents a single ingested file.
    """

    # pylint: disable=too-many-instance-attributes,duplicate-code

    # The attributes that are used in this class to fully describe a data file
    class_attributes = [
        "name",
        "incoming_directory",
        "directory",
        "online",
        "size",
        "checksum_value",
        "checksum_type",
        "time_units",
        "calendar",
        "start_time",
        "end_time",
        "frequency",
        "standard_name",
        "long_name",
        "var_name",
        "units",
        "dimensions",
    ]

    def __init__(self, name, incoming_directory):
        """
        Create a blank observation file object.

        :param str name: The name of the file.
        :param str incoming_directory: The path to the directory containing
            the file.
        """
        self.name = name
        self.incoming_directory = incoming_directory
        self.directory = incoming_directory
        self.online = True
        self.size = None
        self.checksum_value = None
        self.checksum_type = None
        self.time_units = None
        self.calendar = None
        self.start_time = None
        self.end_time = None
        self.frequency = None
        self.standard_name = None
        self.long_name = None
        self.var_name = None
        self.units = ""
        self.dimensions = None

    def add_metadata(self):
        """
        Load a file and gather as much metadata from it as possible.
        """
        logger.debug(f"Getting metadata for {self.name}")
        filepath = os.path.join(self.directory, self.name)
        self.size = os.path.getsize(filepath)
        self.checksum_value = sha256(filepath)
        self.checksum_type = "SHA256"
        if "_" in self.name:
            freq_string = self.name.split("_")[1]
            for freq in ["yr", "mon", "day", "6hr", "3hr", "1hr"]:
                if freq in freq_string:
                    self.frequency = freq
                    break

        # If it's a netCDF file then we can get extra metadata
        if self.name.endswith(".nc"):
            self._add_netcdf4_metadata()

    def to_django_instance(self, base_url, dataset, username, password):
        """
        Convert this object into a Django dmt_app.models.DataFile
        instance of the same file.

        :param str base_url: The URL of the root of the API on the server ending with
            a forward slash.
        :param str dataset: The URL of the parent dataset in the API.
        :param str password: The password to use in the API call.
        :param str username: The username to use in the API call.
        """
        # Post the new dataset to the server
        json_attributes = {attr: getattr(self, attr) for attr in self.class_attributes}
        json_attributes["dataset"] = dataset

        url = f"{base_url}datafiles/"
        response = requests.post(
            url, json=json_attributes, auth=(username, password), timeout=5.0
        )
        if response.status_code != requests.codes.created:  # pylint: disable=no-member
            msg = (
                f"{response.status_code} ({responses[response.status_code]}) "
                f"response from HTTP POST {response.url} "
                f"{os.path.join(self.incoming_directory, self.name)}"
            )
            raise APIQueryError(msg, server_message=response.text)

    def _add_netcdf4_metadata(self):
        """
        Get as much internal metadata as possible using the netCDF4 library.
        """
        # pylint: disable=too-many-branches
        logger.debug(f"Getting metadata using netCDF4 for {self.name}")
        filepath = os.path.join(self.directory, self.name)
        with Dataset(filepath) as rootgrp:
            if "time" in rootgrp.dimensions:
                time_dim = rootgrp["time"]
                try:
                    self.time_units = time_dim.units
                except AttributeError:
                    logger.warning(f"No units for time dimension in {self.name}")
                try:
                    self.calendar = time_dim.calendar
                except AttributeError:
                    logger.warning(
                        f"No calendar for time dimension in {self.name}, "
                        f"assuming gregorian."
                    )
                    self.calendar = "gregorian"
                self.start_time = float(time_dim[:].min())
                self.end_time = float(time_dim[:].max())

            for variable in rootgrp.variables:
                if variable not in rootgrp.dimensions:
                    if not self.var_name:
                        self.var_name = variable
                    else:
                        self.var_name = f"{self.var_name}, {variable}"
                    for var_type in ["long_name", "standard_name", "units"]:
                        if var_type in rootgrp[variable].ncattrs():
                            var_value = rootgrp[variable].getncattr(var_type)
                            if var_type == "units":
                                var_value = str(var_value)
                            if not getattr(self, var_type):
                                setattr(self, var_type, var_value)
                            else:
                                setattr(
                                    self,
                                    var_type,
                                    getattr(self, var_type) + ", " + var_value,
                                )
            # Remove duplicate items from units using set comprehension
            self.units = ", ".join(
                sorted({item.strip() for item in self.units.split(",")})
            )

            for dimension in rootgrp.dimensions:
                if not getattr(self, "dimensions"):
                    setattr(self, "dimensions", dimension)
                else:
                    setattr(
                        self,
                        "dimensions",
                        getattr(self, "dimensions") + ", " + dimension,
                    )
