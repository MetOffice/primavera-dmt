# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of cube_helper and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""Django boilerplate to set-up a Django app"""

from django.apps import AppConfig


class DmtAppConfig(AppConfig):
    """Django boilerplate to set-up the dmt_app app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "dmt_app"
