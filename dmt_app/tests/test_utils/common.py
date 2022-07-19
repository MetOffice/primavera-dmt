# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""Common code used by many tests"""

import os
import tempfile

from netCDF4 import Dataset as NCDataset  # pylint: disable=no-name-in-module

from dmt_app.models import DataFile, DataSet


class SampleDjangoEntities:
    """Make sample DataSet and DataFile"""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        """Create base object"""
        self.dataset = None
        self.datafile1 = None
        self.datafile2 = None
        self.dataset_attrs = {"name": "OBS", "version": "1"}
        self.datafile1_attrs = {
            "name": "file1.nc",
            "incoming_directory": "/some/dir",
            "size": 1,
            "checksum_value": "abcdef",
            "checksum_type": "MD5",
            "online": True,
        }
        self.datafile2_attrs = {
            "name": "file2.nc",
            "incoming_directory": "/other/dir",
            "size": 2,
            "checksum_value": "123456",
            "checksum_type": "SHA256",
            "online": False,
        }

    def make_django_entities(self):
        """Make sample DataSet and DataFile"""
        self.dataset = DataSet.objects.create(**self.dataset_attrs)
        self.datafile1 = DataFile.objects.create(
            dataset=self.dataset, **self.datafile1_attrs
        )
        self.datafile2 = DataFile.objects.create(
            dataset=self.dataset, **self.datafile2_attrs
        )
        return self


def make_sample_netcdf(filename):
    """
    Generate a sample netCDF file with the specified name.

    :param str filename: The full path of the netCDF file to create
    """
    _fd, cdl_filename = tempfile.mkstemp(suffix=".cdl")
    with open(cdl_filename, "w", encoding="utf-8") as hndl:
        hndl.writelines(REALISTIC_NETCDF_CDL)
    NCDataset.fromcdl(cdl_filename, filename)
    os.remove(cdl_filename)


REALISTIC_NETCDF_CDL = """
netcdf realistic_3d {
dimensions:
    time = 4 ;
    grid_latitude = 3 ;
    grid_longitude = 2 ;
variables:
    int64 so(time, grid_latitude, grid_longitude) ;
        so:long_name = "Sea Water Salinity" ;
        so:standard_name = "sea_water_salinity" ;
        so:units = "0.001" ;
    int64 tas(time, grid_latitude, grid_longitude) ;
        tas:long_name = "Near-Surface Air Temperature" ;
        tas:standard_name = "air_temperature" ;
        tas:units = "K" ;
    int64 tos(time, grid_latitude, grid_longitude) ;
        tos:standard_name = "sea_surface_temperature" ;
        tos:units = "K" ;
    double time(time) ;
        time:axis = "T" ;
        time:units = "hours since 1970-01-01 00:00:00" ;
        time:standard_name = "time" ;
        time:calendar = "gregorian" ;
    double grid_latitude(grid_latitude) ;
        grid_latitude:axis = "Y" ;
        grid_latitude:units = "degrees" ;
        grid_latitude:standard_name = "grid_latitude" ;
    double grid_longitude(grid_longitude) ;
        grid_longitude:axis = "X" ;
        grid_longitude:units = "degrees" ;
        grid_longitude:standard_name = "grid_longitude" ;

// global attributes:
        :source = "Iris test case" ;
        :Conventions = "CF-1.7" ;
data:

 so =
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
  11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
  22, 23 ;

 tas =
  100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
  111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121,
  122, 123 ;

 tos =
  200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210,
  211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221,
  222, 223 ;

 time = 394200, 394224, 394248, 394272 ;

 grid_latitude = -2, 1, 4 ;

 grid_longitude = -5, 5 ;
}
"""
