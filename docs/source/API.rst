===========
RESTful API
===========

The DMT includes a RESTful API to allow programmatic access to the datasets and files in
the DMT. By default the API is available at ``/api/``. The API includes a web browsable
interface to the API to allow developers to test it.

The browsable interface self-documents the API. There is an additional parameter called
`page_size` available to allow users to set the number of results returned (up to the
maximum configured). For example ``/api/datafiles/?page=5&page_size=1``.





