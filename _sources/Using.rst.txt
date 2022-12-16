=======================
Using the web interface
=======================

The Data Management Tool (DMT) contains two fundamental data entities:

Data Sets
    Collections of data files that are combined together with metadata such as the
    license that the data is available under, a summary, a reference and a DOI.
    This metadata is manually added to each data set by DMT administrators.

Data Files
    Individual files make up a data set. Details of each file such as its name, path,
    size and checksum are recorded. Additional, metadata is available for netCDF files
    such as its variables, dimensions, units and start and end times.

Table views of data sets and data files are linked from the DMT's front page and
also from the drop down menu in the title bar.

On each page there are text boxes to filter the entities using various common
metadata attributes. To filter entities, enter text into one or more text boxes and then
click the `Filter` button. Clicking the `Clear` button clears all of the search terms
and shows all rows again. All search terms are case insensitive and match on values
that contain the search term (as opposed to being an exact match).

The order of entities in the tables can be sorted by clicking
on the arrow in the column headers. Clicking on an arrow a second time will reverse the
sort order. Due to limitations in how metadata is stored in the DMT's database, it is not
possible to order some columns.

In the Data Sets view, clicking on the number in the `# Data Files` column will take you
to page that shows just the data files for that data set.