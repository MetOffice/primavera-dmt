# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

from django.db import models
from django.db.models import CASCADE

from .vocabs import CHECKSUM_TYPES


class DataSet(models.Model):
    """
    Django model to represent a set of data files.
    """
    class Meta:
        unique_together = ('name', 'version')
        verbose_name = 'Dataset'

    # Compulsory attributes
    name = models.CharField(max_length=200, verbose_name='Name', blank=False)
    version = models.CharField(max_length=200, verbose_name='Version',
                               blank=True, null=True)
    # Additional optional attributes
    url = models.URLField(verbose_name='URL', null=True, blank=True)
    summary = models.CharField(max_length=4000, verbose_name='Summary',
                               null=True, blank=True)
    doi = models.CharField(max_length=200, verbose_name='DOI',
                           null=True, blank=True)
    reference = models.CharField(max_length=4000, verbose_name='Reference',
                                 null=True, blank=True)
    license = models.URLField(verbose_name='License', null=True, blank=True)
    date_downloaded = models.DateTimeField(verbose_name='Date downloaded',
                                           null=True, blank=True)
    creator = models.CharField(max_length=100, verbose_name='Creator',
                               null=True, blank=True)

    @property
    def online_status(self):
        """
        Checks aggregation of online status of all DataFiles.
        Returns one of: online, offline, partial
        """
        files_online = self.datafile_set.filter(online=True).count()
        files_offline = self.datafile_set.filter(online=False).count()

        if files_offline:
            if files_online:
                return 'partial'
            else:
                return 'offline'
        else:
            return 'online'

    def __str__(self):
        return f'{self.name} ({self.version})' if self.version else self.name


class DataFile(models.Model):
    """
    Django model to represent a DataFile.
    """
    class Meta:
        unique_together = ('name', 'incoming_directory')
        verbose_name = 'Data File'

    name = models.CharField(max_length=255, verbose_name='File name',
                            blank=False)
    incoming_directory = models.CharField(max_length=4096,
                                          verbose_name='Incoming directory',
                                          blank=False)
    directory = models.CharField(max_length=4096, verbose_name='Directory',
                                 blank=True, null=True)
    size = models.BigIntegerField(verbose_name='File size')

    checksum_value = models.CharField(max_length=200, blank=False)
    checksum_type = models.CharField(max_length=20, choices=CHECKSUM_TYPES,
                                     blank=False)

    online = models.BooleanField(default=True, blank=False,
                                 verbose_name='Online?')

    # Foreign Key Relationships
    dataset = models.ForeignKey(DataSet, blank=False,
                                on_delete=CASCADE, verbose_name='Dataset')

    def __str__(self):
        return f'{self.name} (Directory: {self.directory})'
