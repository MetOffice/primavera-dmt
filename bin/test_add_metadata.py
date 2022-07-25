#!/usr/bin/env python

# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
test_add_metadata.py

To test web display add some metadata to one dataset
"""
import datetime
import django

django.setup()
from dmt_app.models import DataSet  # noqa # pylint: disable=wrong-import-position


def main():
    """main entry"""
    dataset = DataSet.objects.get(name="COMORPH")
    dataset.doi = "10.25921/w9va-q159"
    dataset.reference = (
        "Joyce, R. J., J. E. Janowiak, P. A. Arkin, and P. Xie, "
        "2004: CMORPH: A method that produces global precipitation "
        "estimates from passive microwave and infrared data at "
        "high spatial and temporal resolution.. J. Hydromet., 5, "
        "487-503."
    )
    dataset.url = (
        "https://www.ncei.noaa.gov/products/climate-data-records/"
        "precipitation-cmorph"
    )
    dataset.license = (
        "https://ncei.noaa.gov/pub/data/sds/cdr/CDRs/Precipitation-"
        "CMORPH/UseAgreement_01B-23.pdf"
    )
    dataset.date_downloaded = datetime.datetime(
        1978, 7, 19, 1, 2, 3, 0, datetime.timezone(datetime.timedelta(0))
    )
    dataset.save()


if __name__ == "__main__":
    main()
