#!/usr/bin/env python
"""
ingest_dataset.py

Capture the metadata from a dataset and add this to the database.
"""
import argparse
import logging
import sys

import django
django.setup()

from dmt_app.utils.ingestion import (APIQueryError, CredentialsFileError,
                                     DmtCredentials, IngestedDataset)  # noqa


__version__ = '0.1.0b1'

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)

# The path to a users DMT settings file where their credentials and the API URL
#  are stored
DMT_SETTINGS_FILE = '~/.config/dmt/dmt.json'


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Ingest a dataset into the DMT')
    parser.add_argument('-l', '--log-level',
                        help='set logging level to one of debug, info, warn '
                             '(the default), or error')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument('directory', help="The dataset's "
                                          "top-level directory")
    parser.add_argument('name', help="The dataset's name")
    parser.add_argument('dataset_version', help="The dataset's version")
    parser.add_argument('-a', '--all', action='store_true',
                        help='add metadata for all files, not just netCDF')
    args = parser.parse_args()

    return args


def main(args):
    """
    Main entry point
    """
    try:
        credentials = DmtCredentials(DMT_SETTINGS_FILE)
    except CredentialsFileError as exc:
        logger.error(exc)
        sys.exit(1)

    try:
        dataset = IngestedDataset(args.name, args.dataset_version,
                                  args.directory)
        if args.all:
            dataset.add_files()
        else:
            dataset.add_files(only_netcdf=True)
    except ValueError as exc:
        logger.error(exc)
        sys.exit(1)

    try:
        dataset.to_django_instance(credentials.url, credentials.username,
                                   credentials.password)
    except APIQueryError as exc:
        logger.error(exc)
        if exc.server_message:
            logger.error(exc.server_message)
        sys.exit(1)


if __name__ == "__main__":
    cmd_args = parse_args()

    # determine the log level
    if cmd_args.log_level:
        try:
            log_level = getattr(logging, cmd_args.log_level.upper())
        except AttributeError:
            logger.setLevel(logging.WARNING)
            logger.error('log-level must be one of: debug, info, warn '
                         'or error')
            sys.exit(1)
    else:
        log_level = DEFAULT_LOG_LEVEL

    # configure the logger
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': DEFAULT_LOG_FORMAT,
            },
        },
        'handlers': {
            'default': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': log_level,
                'propagate': True
            }
        }
    })

    # run the code
    main(cmd_args)
