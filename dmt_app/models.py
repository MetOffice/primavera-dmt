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

    name = models.CharField(max_length=200, verbose_name='Name', blank=False)
    version = models.CharField(max_length=200, verbose_name='Version',
                               blank=True)

    def __str__(self):
        return f'{self.name} ({self.version})'


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
                                 blank=True)
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
