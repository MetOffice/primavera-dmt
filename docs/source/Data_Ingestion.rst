============================
Ingesting files into the DMT
============================

Users who have been been granted `Staff` access can use the `ingest_dmt_dataset.py` tool
to ingest a data set and its data files into the DMT. The usage of this tool is::

    usage: ingest_dmt_dataset.py [-h] [-l LOG_LEVEL] [--version] [-a]
                                 directory name dataset_version

    Ingest a dataset into the DMT

    positional arguments:
      directory             The dataset's top-level directory
      name                  The dataset's name
      dataset_version       The dataset's version

    optional arguments:
      -h, --help            show this help message and exit
      -l LOG_LEVEL, --log-level LOG_LEVEL
                            set logging level to one of debug, info, warn (the
                            default), or error
      --version             show program's version number and exit
      -a, --all             add metadata for all files, not just netCDF

A data set consists of a top-level directory and then data files in the directory
structure below this top-level directory. A data set is created by specifying the path
of the top-level directory and a unique name and version string. If the the name or
version contain spaces then they should be quoted, for example::

    ingest_dmt_dataset.py /some/dir "Long Dataset Name"  "V2 (beta)"

By default only files with a `.nc` suffix (netCDF files) are ingested into the data set
but the `--all` option will ingest all data files.


Only the two items of metadata specified on the command line are recorded for each
data set:

* Name
* Version

For each file the following metadata items are recorded:

* Name
* Path
* Size
* SHA256 checksum

Additionally for netCDF files with a .nc suffix the following metadata items are
recorded (where they exist):

* Start date
* End date
* Standard name
* Long name
* Variable name
* Units
* Dimensions

For compactness in the tables, only one form of the names for the variable are displayed
in the table. The following priority order is used when deciding which form to display:

#. Standard name
#. Long name
#. Variable name

However, the "Variables" filter box checks whether any of the three forms of variable
names contains the specified text.

``ingest_dmt_dataset.py`` parses each file in a serial fashion, stores the metadata in
memory and then writes the metadata to the database when all files have been parsed.
The current implementation works well for datasets of several thousand files but does
not scale to datasets of 0.5 million files. The performance of the ingest tool will be
improved in a future version. Please raise `an issue
<https://github.com/MetOffice/primavera-dmt/issues/new>`_ if it is necessary to ingest
a large dataset.

Adding additional metadata to datasets
======================================

Only the minimal number of metadata items mentioned earlier are collected for data sets
during the ingestion process. Additional metadata can be added and edited by super users
using the admin interface at ``https://<server-name>/admin/dmt_app/dataset/`` and then
clicking on the appropriate data set's name.

The following metadata items can be added:

+-----------------+----------+
| Name            | Type     |
+=================+==========+
| URL             | URL      |
+-----------------+----------+
| Summary         | String   |
+-----------------+----------+
| DOI             | String   |
+-----------------+----------+
| Reference       | String   |
+-----------------+----------+
| License         | URL      |
+-----------------+----------+
| Date downloaded | Datetime |
+-----------------+----------+
| Project         | String   |
+-----------------+----------+

Authentication
==============

The DMT's super user will create a username and password for each `Staff` user as
described in :doc:`Installing`. Ordinary users browsing the DMT do not need a username
or password. These credentials must be stored in a file called `~/.config/dmt/dmt.json`
in a `Staff` user's home directory. This file must have permissions of 400 (i.e. read
permission for just the owner) or else the ingest tool will not run. The structure of
this credentials file is::

    {
        "url": "http://<server name>/api/",
        "username": "<username>",
        "password": "<password>"
    }



