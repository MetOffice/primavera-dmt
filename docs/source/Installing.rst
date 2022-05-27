==========================
Installing and Configuring
==========================

`primavera_dmt` is available from https://github.com/MetOffice/primavera_dmt

Installation on a server can be achieved in a similar way to the method described in
the :doc:`Developing`. This process is often automated using
`Ansible playbooks <https://www.ansible.com/>`_, for example
https://github.com/cedadev/ansible-cedatest.

Admin Interface
===============

The Django Admin interface provides a convenient way for authorised users to add and
edit metadata on ingested data. By default users don't have access to the Admin interface
until they have been given `Staff` access by a `Superuser`. Once granted `Staff` access
then additional permissions need to be granted to allow them to edit and view specified
data objects.

Initial Admin Interface Configuration
=====================================

The setup of users, groups and the necessary permissions in the Admin interface has not
been automated and needs to be done manually once for each installation. The steps to
do this are:

#. If not only done during the initial installation, create a superuser::

    django-admin createsuperuser

#. In a browser open the admin interface at  ``https://<server-name>/admin/`` and login as the
   superuser that was just created.

#. Navigate to ``Authentication and Authorization`` and then ``Groups`` and then click on
   ``Add``.

#. Enter a suitable name, such as `data_editor` and then select the eight permissions::

    dmt_app | Data File | Can add Data File
    dmt_app | Data File | Can change Data File
    dmt_app | Data File | Can delete Data File
    dmt_app | Data File | Can view Data File
    dmt_app | Dataset | Can add Dataset
    dmt_app | Dataset | Can change Dataset
    dmt_app | Dataset | Can delete Dataset
    dmt_app | Dataset | Can view Dataset

   and then click on the right arrow to move these into the `Chosen permissions` column and
   then click on ``Save``.

Adding Users
============

#. In the Admin interface at ``https://<server-name>/admin/`` navigate to
   ``Authentication and Authorization`` and then ``Users`` and then click on
   ``Add``. Enter an appropriate username and password and then click on ``Save``.

#. In the subsequent `Change user` page select the ``Staff status`` box and in the `Groups`
   box select the data editor group created during the initial configuration, for example
   ``data_editor`` and then click on the right arrow to move this into the `Chosen groups`
   column. Finally click on ``Save`` at the bottom of the page.

#. Create a ``~/.config/dmt/dmt.json`` file....



