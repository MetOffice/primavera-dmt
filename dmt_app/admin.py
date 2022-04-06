from django.contrib import admin

from dmt_app.models import DataFile, DataSet

# Register your models here.
admin.site.register(DataFile)
admin.site.register(DataSet)