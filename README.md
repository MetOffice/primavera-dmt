# primavera-dmt
PRIMAVERA Data Management Tool

A Python and Django based data management tool and catalogue developed from
https://github.com/PRIMAVERA-H2020/primavera-dmt.

## Contributing  
If you want to contribute to primavera-dmt be sure to review the
[contribution guidelines](https://github.com/MetOffice/primavera-dmt/blob/master/CONTRIBUTING.md).

## License
[BSD-3 License](https://github.com/MetOffice/primavera-dmt/blob/master/LICENSE)

## Quick set-up

1. Load a Conda or virtualenv environment containing:   
   ```  
   django  
   django-filter  
   django-tables2
   djangorestframework
   numpy
   netCDF4
   requests
   ```  
   
   For example in a Python virtual environment:
   ```
   mkdir ../venvs
   python3 -m venv ../venvs/django --system-site-packages
   . ../venvs/django/Scripts/activate
   pip install -r requirements.txt 
   ```
 
   
2. Create local settings:    
   ```  
   cp dmt_site/local_settings.py.tmpl dmt_site/local_settings.py  
    ``` 
   Populate the value of `SECRET_KEY` on line 43 of `dmt_site/local_settings.py`
   with a suitable random string. A string can be generated from the command line:
   ```
   $ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

3. Django set-up and create databases:  
   ```
   export DJANGO_SETTINGS_MODULE=dmt_site.settings
   export PYTHONPATH=.
   django-admin makemigrations dmt_app
   django-admin migrate
   ```

4. Run tests:
   ```
   django-admin test
   ```
   
5. View the website in a local development server:
   In `dmt_site/settings.py` enable debug mode by changing line 24 to:
   ```
   DEBUG = True
   ```
   Start the development server:
   ```
   django-admin runserver
   ```
   Point your browser at `http://localhost:8000/` to view the site.
