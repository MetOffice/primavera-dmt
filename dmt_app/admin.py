# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""Django boilerplate to add the dmt_app app to the admin site"""

from django.contrib import admin

from dmt_app.models import DataFile, DataSet

# Register your models here.
admin.site.register(DataFile)
admin.site.register(DataSet)
