# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
Define tables to display dmt_app models using django_tables2.
"""
import datetime
from urllib.parse import urlencode

from django.template.defaultfilters import filesizeformat
from django.utils.html import format_html
from django.urls import reverse
import django_tables2 as tables

from .models import DataFile, DataSet

# The string to display if a value doesn't exist
DEFAULT_VALUE = "—"


class DataFileTable(tables.Table):
    """
    Table to display dmt_app.models.DataFile
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """Django model metadata"""

        model = DataFile
        attrs = {"class": "paleblue"}
        exclude = (
            "id",
            "incoming_directory",
            "dataset",
            "checksum_value",
            "checksum_type",
        )
        sequence = ["name", "directory", "online", "size", "checksum"]
        order_by = "name"

    checksum = tables.Column(empty_values=(), verbose_name="Checksum", orderable=False)

    def render_checksum(self, record):  # pylint: disable=no-self-use
        """Render the checksum nicely"""
        return f"{record.checksum_type}: {record.checksum_value}"

    def render_size(self, value):  # pylint: disable=no-self-use
        """Display the file's size in a human-readable form"""
        return filesizeformat(value)


class DataSetTable(tables.Table):
    """
    Table to display dmt_app.models.DataSet
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """Django model metadata"""

        model = DataSet
        attrs = {"class": "paleblue"}
        exclude = ("id", "creator")
        sequence = [
            "name",
            "version",
            "num_files",
            "online_status",
            "summary",
            "url",
            "doi",
            "license",
            "reference",
            "date_downloaded",
        ]
        order_by = "name"

    num_files = tables.Column(
        empty_values=(), verbose_name="# Data Files", orderable=False
    )
    online_status = tables.Column(empty_values=(), orderable=False)

    def render_num_files(self, record):  # pylint: disable=no-self-use
        """Allow the number of files to link to the set's files"""
        num_datafiles = record.datafile_set.count()
        url_query = urlencode(
            {
                "dataset": record.id,
                "dataset_string": f"{record.name} ({record.version})",
            }
        )
        return format_html(
            f'<a href="{reverse("datafiles")}?{url_query}">{num_datafiles}</a>'
        )

    def render_date_downloaded(self, value):  # pylint: disable=no-self-use
        """Display the date as DD/MM/YYYY"""
        if isinstance(value, datetime.datetime):
            return value.strftime("%Y-%m-%d")
        return DEFAULT_VALUE

    def render_doi(self, value):  # pylint: disable=no-self-use
        """Render the DOI as a working hyperlink"""
        return format_html(f'<a href="https://doi.org/{value}">{value}</a>')
