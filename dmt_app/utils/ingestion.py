"""
Various classes to ingest datasets into the DMT
"""
import logging
import os


from netCDF4 import Dataset

from dmt_app.models import DataSet, DataFile
from dmt_app.utils.common import list_files, sha256


logger = logging.getLogger(__name__)


class IngestedDataset(object):
    """
    An ingested data set that can have files added to it and can then be added
    to the database.
    """
    # The attributes that are required in the class to fully describe a
    # data set
    class_attributes = ['name', 'version', 'incoming_directory']
    django_attributes = ['name', 'version']

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
            msg = f'Directory does not exist: {incoming_directory}'
            raise ValueError(msg)

        if not os.path.isdir(incoming_directory):
            msg = f'Path is not a directory: {incoming_directory}'
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
            found_files = list_files(self.incoming_directory)
        else:
            found_files = list_files(self.incoming_directory, '')

        if not found_files:
            msg = ('No files found in directory or its subdirectories '
                   '{}'.format(self.incoming_directory))
            raise ValueError(msg)

        logger.debug('{} files identified'.format(len(found_files)))

        for found_file in found_files:
            data_file = IngestedDatafile(os.path.basename(found_file),
                                         os.path.dirname(found_file))
            data_file.add_metadata()
            self.datafiles.append(data_file)

        logger.debug('{} files added'.format(len(self.datafiles)))

    def to_django_instance(self):
        """
        Convert this object into a Django pdata_app.models.ObservationDataset
        instance of the same observations set. Instances of each file in the
        set are also created.
        """
        django_set = DataSet.objects.create(
            **{attr: getattr(self, attr) for attr in self.django_attributes}
        )
        for datafile_obj in self.datafiles:
            # TODO add to_django_instance to file class
            DataFile.objects.create(
                dataset=django_set,
                **{attr: getattr(datafile_obj, attr)
                   for attr in datafile_obj.class_attributes}
            )


class IngestedDatafile(object):
    """
    A class that represents a single ingested file.
    """
    # The attributes that are used in the class to fully describe a
    # data file
    class_attributes = ['name', 'incoming_directory', 'directory', 'online',
                        'size', 'checksum_value', 'checksum_type']

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

    def add_metadata(self):
        """
        Load a file and gather as much metadata from it as possible.
        """
        logger.debug('Getting metadata for {}'.format(self.name))
        filepath = os.path.join(self.directory, self.name)
        self.size = os.path.getsize(filepath)
        self.checksum_value = sha256(filepath)
        self.checksum_type = 'SHA256'
        # if '_' in self.name:
        #     freq_string = self.name.split('_')[1]
        #     for freq in ['yr', 'mon', 'day', '6hr', '3hr', '1hr']:
        #         if freq in freq_string:
        #             self.frequency = freq
        #             break

        # If it's a netCDF file then we can get extra metadata
        # if self.name.endswith('.nc'):
        #     logger.debug('Getting additional netCDF metadata for {}'.
        #                  format(self.name))
        #     self._add_netcdf4_metadata()

    def _add_netcdf4_metadata(self):
        """
        Get as much internal metadata as possible using the netCDF4 library.
        """
        logger.debug('Getting metadata using netCDF4 for {}'.format(self.name))
        filepath = os.path.join(self.directory, self.name)
        with Dataset(filepath) as rootgrp:
            if 'time' in rootgrp.dimensions:
                time_dim = rootgrp['time']
                self.time_units = time_dim.units
                self.calendar = time_dim.calendar
                self.start_time = float(time_dim[:].min())
                self.end_time = float(time_dim[:].max())

            for variable in rootgrp.variables:
                if variable not in rootgrp.dimensions:
                    for var_type in ['var_name', 'long_name', 'standard_name',
                                     'units']:
                        if var_type in rootgrp[variable].ncattrs():
                            var_value = rootgrp[variable].getncattr(var_type)
                            if var_type == 'units':
                                var_value = str(var_value)
                            if not getattr(self, var_type):
                                setattr(self, var_type, var_value)
                            else:
                                setattr(self, var_type,
                                        getattr(self, var_type) + ', ' +
                                        var_value)
