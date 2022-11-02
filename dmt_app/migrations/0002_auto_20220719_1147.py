# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

# Generated by Django 3.2 on 2022-07-19 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dmt_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datafile",
            name="dimensions",
            field=models.CharField(
                blank=True, max_length=2000, null=True, verbose_name="Dimensions"
            ),
        ),
        migrations.AlterField(
            model_name="datafile",
            name="long_name",
            field=models.CharField(
                blank=True, max_length=10000, null=True, verbose_name="Long name"
            ),
        ),
        migrations.AlterField(
            model_name="datafile",
            name="standard_name",
            field=models.CharField(
                blank=True, max_length=2000, null=True, verbose_name="Standard name"
            ),
        ),
        migrations.AlterField(
            model_name="datafile",
            name="units",
            field=models.CharField(
                blank=True, max_length=2000, null=True, verbose_name="Units"
            ),
        ),
        migrations.AlterField(
            model_name="datafile",
            name="var_name",
            field=models.CharField(
                blank=True, max_length=2000, null=True, verbose_name="Var name"
            ),
        ),
    ]
