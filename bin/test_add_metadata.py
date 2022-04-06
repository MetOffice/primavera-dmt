#!/usr/bin/env python
"""
test_add_metadata.py

To test web display add some metadata to one dataset
"""
import datetime
import django
django.setup()
from dmt_app.models import DataSet  # noqa


def main():
    """main entry"""
    ds = DataSet.objects.get(name="COMORPH")
    ds.doi = "10.25921/w9va-q159"
    ds.reference = ("Joyce, R. J., J. E. Janowiak, P. A. Arkin, and P. Xie, "
                    "2004: CMORPH: A method that produces global precipitation "
                    "estimates from passive microwave and infrared data at "
                    "high spatial and temporal resolution.. J. Hydromet., 5, "
                    "487-503.")
    ds.url = ("https://www.ncei.noaa.gov/products/climate-data-records/"
              "precipitation-cmorph")
    ds.license = ("https://ncei.noaa.gov/pub/data/sds/cdr/CDRs/Precipitation-"
                  "CMORPH/UseAgreement_01B-23.pdf")
    ds.date_downloaded = datetime.datetime(1978, 7, 19, 1, 2, 3, 0,
                                           datetime.timezone(
                                               datetime.timedelta(0)))
    ds.save()

if __name__ == "__main__":
    main()
