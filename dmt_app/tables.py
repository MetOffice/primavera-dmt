# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
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
            "checksum_value",
            "checksum_type",
            "time_units",
            "calendar",
            "standard_name",
            "long_name",
            "var_name",
            "start_time",
            "end_time",
        )
        sequence = [
            "name",
            "directory",
            "dataset",
            "variables",
            "start_string",
            "end_string",
            "frequency",
            "units",
            "dimensions",
            "online",
            "size",
            "project",
            "checksum",
        ]
        order_by = "name"

    dataset = tables.Column(empty_values=(), verbose_name="Data Set", orderable=True)
    variables = tables.Column(
        empty_values=(), verbose_name="Variables", orderable=False
    )
    checksum = tables.Column(empty_values=(), verbose_name="Checksum", orderable=False)
    project = tables.Column(empty_values=(), verbose_name="Project", orderable=True)
    start_string = tables.Column(
        empty_values=(), verbose_name="Starts", orderable=False
    )
    end_string = tables.Column(empty_values=(), verbose_name="Ends", orderable=False)

    def render_dataset(self, record):  # pylint: disable=no-self-use
        """Render the parent data set's name"""
        return f"{record.dataset.name} ({record.dataset.version})"

    def order_dataset(self, queryset, is_descending):  # pylint: disable=no-self-use
        """Allow the files to be ordered by dataset name then version"""
        queryset = queryset.order_by(
            ("-" if is_descending else "") + "dataset__name",
            ("-" if is_descending else "") + "dataset__version",
        )
        return (queryset, True)

    def render_variables(self, record):  # pylint: disable=no-self-use
        """Render the names of the variables in the file"""
        if record.variables:
            return record.variables
        return DEFAULT_VALUE

    def render_checksum(self, record):  # pylint: disable=no-self-use
        """Render the checksum nicely"""
        return f"{record.checksum_type}: {record.checksum_value}"

    def render_size(self, value):  # pylint: disable=no-self-use
        """Display the file's size in a human-readable form"""
        return filesizeformat(value)

    def render_project(self, record):  # pylint: disable=no-self-use
        """Display the parent dataset's project attribute"""
        if record.dataset.project:
            return record.dataset.project
        return DEFAULT_VALUE

    def order_project(self, queryset, is_descending):  # pylint: disable=no-self-use
        """Allow the files to be ordered by project"""
        queryset = queryset.order_by(
            ("-" if is_descending else "") + "dataset__project"
        )
        return (queryset, True)

    def render_start_string(self, record):  # pylint: disable=no-self-use
        """Display the start string"""
        if record.start_string:
            return record.start_string
        return DEFAULT_VALUE

    def render_end_string(self, record):  # pylint: disable=no-self-use
        """Display the end string"""
        if record.end_string:
            return record.end_string
        return DEFAULT_VALUE


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
            "project",
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
                "dataset_id": record.id,
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
