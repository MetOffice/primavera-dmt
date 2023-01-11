========================
Developers' Instructions
========================


Quick set-up
============

#. Load a Conda or virtualenv environment containing::

    argon2-cffi
    cftime
    django
    django-filter
    django-tables2
    djangorestframework
    numpy
    netCDF4
    requests

   For example in a Python virtual environment::

    mkdir ../venvs
    python3 -m venv ../venvs/django --system-site-packages
    . ../venvs/django/Scripts/activate
    pip install -r requirements.txt

   `psycopg2` is included in `requirements.txt` as it is needed in the production
   version where a PostgreSQL database is used rather than SQLite.


#. Create local settings::

    cp dmt_site/local_settings.py.tmpl dmt_site/local_settings.py

   Populate the value of ``SECRET_KEY`` in ``dmt_site/local_settings.py``
   with a suitable random string. A string can be generated from the command line::

    $ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

#. Django set-up and create databases::

    export DJANGO_SETTINGS_MODULE=dmt_site.settings
    export PYTHONPATH=.
    django-admin makemigrations dmt_app
    django-admin migrate

#. Create a superuser so that the admin interface can be used::

    django-admin createsuperuser

#. Run tests::

    django-admin test

#. View the website in a local development server:
   In `dmt_site/settings.py` enable debug mode by setting ``DEBUG`` to::

    DEBUG = True

   Start the development server::

    django-admin runserver

   Point your browser at http://localhost:8000/ to view the site.

Test Environment
================

Running the unit tests requires the ncgen utility to be installed. For the GitHub Actions
continuous integration tests it is installed with the following commands::

    sudo apt-get update
    sudo apt-get install netcdf-bin

ncgen is commonly installed on many scientific Linux system.

Continuous Integration
======================

GitHub Actions runs seven tests on every commit to a pull request to ensure code
quality. This number of tests may seem excessive but experience has shown that each
spots different issues with the code and this number provides a higher level of
reassurance in the code's quality. It may be worth running black locally and then
monitoring the output from GitHub Actions to find any issues that need to be fixed,
although all of the tests can be installed and run locally too.

The tests that are run are:

+--------------+------------------------------+----------------------------------------+
| Test type    | Why?                         | How?                                   |
+==============+==============================+========================================+
| Django Tests | Run the unit tests           | ``django-admin test``                  |
+--------------+------------------------------+----------------------------------------+
| Black        | Ensure consistent formatting | ``black --check .``                    |
+--------------+------------------------------+----------------------------------------+
| Pylint       | Code quality                 | [see below]                            |
+--------------+------------------------------+----------------------------------------+
| Flake8       | Style checking               | ``flake8 .``                           |
+--------------+------------------------------+----------------------------------------+
| Pycodestyle  | Style checking               | ``pycodestyle --max-line-length=88 .`` |
+--------------+------------------------------+----------------------------------------+
| Docs build   | Check docs build             | ``make html``                          |
+--------------+------------------------------+----------------------------------------+
| Bandit       | Security issues              | ``bandit -r .``                        |
+--------------+------------------------------+----------------------------------------+

Pylint has to be run four times, once in each directory::

    pylint dmt_app
    pylint dmt_site
    pylint bin
    pylint docs/source/conf.py

There are configuration files in the root of the repository that configure Flake8 and
Pylint.

Documentation
=============

The documentation is stored in the `gh-pages` branch of the repository and served at 
https://metoffice.github.io/primavera-dmt/ using `GitHub Pages <https://pages.github.com/>`_. 
`gh-pages` is not a branch in the traditional sense of Git branches as it does not contain
any of the contents of the `main` branch, just a copy of the built HTML documentation.

Changes to the documentation can be published with the following steps.

#. In the `main` branch, or preferably a branch of `main`, make the changes that you
   require to the files in the `docs/` directory.

#. Build the documentation by opening a Python environment that contains 
   `Sphinx <https://www.sphinx-doc.org/>`_ and then type::

    cd docs
    make clean && make html

#. Check the local copy of the documentation (Firefox is used here but any 
   browser is acceptable)::
    
    firefox build/html/index.html

#. When happy with your changes, follow your usual workflow to commit this change 
   to the main branch.

#. Create a new clone of the repository and branch the `gh-pages` branch::

    cd ../..
    git clone git@github.com:MetOffice/primavera-dmt.git primavera-dmt-pages
    cd primavera-dmt-pages
    git branch my-new-doc-version origin/gh-pages
    git checkout my-new-doc-version

#. Copy the new built documentation into the branch, commit and push to the 
   repository::

    cp -R ../primavera-dmt/docs/build/html/* .
    git status
    git commit -am 'My new documentation version'
    git push origin my-new-doc-version

#. Create a new pull request at https://github.com/MetOffice/primavera-dmt/compare
   and ensure that you are committing your `my-new-doc-version` branch into the `gh-pages`
   branch. Review the pull request, merge and then check the result at 
   https://metoffice.github.io/primavera-dmt/.