# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of primavera-dmt and is released under the
# BSD 3-Clause license.
# See LICENSE in the root of the repository for full licensing details.

"""
A custom class for drawing tables from QuerySets

Taken from: http://stackoverflow.com/questions/25256239/\
how-do-i-filter-tables-with-django-generic-views
"""

from django_tables2 import SingleTableView


class PagedFilteredTableView(SingleTableView):
    # pylint: disable=attribute-defined-outside-init, missing-class-docstring
    # pylint: disable=super-with-arguments, too-many-ancestors
    filter_class = None
    context_filter_name = "filter"
    page_title = None
    title_bar_text = None

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        # pylint: disable=not-callable
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context["page_title"] = self.page_title
        context["title_bar_text"] = self.title_bar_text
        return context
