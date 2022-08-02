# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.
"""
Allow the DMT to be installed into a virtualenv
"""

from setuptools import setup, find_packages


VERSION = "1.0.1"

setup(
    name="dmt_site",
    version=VERSION,
    description="PRIMAVERA Data Management Tool",
    url="https://github.com/PRIMAVERA-H2020/primavera-dmt",
    packages=find_packages(),
    include_package_data=True,
)
