Platforms Overseer
==================

An app which spiders all our Github repos, collects data on software library and
application dependencies and can report on which products have specified
dependencies.

Installation
------------

You will need:

* `Python 2.7`_
* `virtualenvwrapper`_

.. _Python 2.7: https://www.python.org/downloads/release/python-2710/
.. _virtualenvwrapper: https://pypi.python.org/pypi/virtualenvwrapper

Clone the repository::

    git clone git@github.com:ministryofjustice/po

Create a virtualenv and install the dependencies::

    cd po
    mkvirtualenv po
    pip install -r requirements.txt

Run migrations and create a superuser::

    ./manage.py migrate
    ./manage.py createsuperuser

Run the server::

    ./manage.py runserver

Access the server at http://localhost:8000/

And the admin at http://localhost:8000/admin/


Configuration
-------------


Usage
-----

Submitting APT dependency information for a deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To automatically submit APT package dependencies for an app on deployment by
Jenkins (or other CI system), a build step needs to call the
`scripts/post-dependencies.sh` script.

This script will query `dpkg` for a list of installed packages, generate a JSON
payload and POST it to the Platform Overseer API.

The following environment variables need to be set:

  * **PROJECT** - the name of the project/app
  * **APP_BUILD_TAG** - the name of the build (tries BUILD_TAG if not set)
  * **ENV** - the name of the deployment environment, eg: staging


Support
-------


Contributing
------------


Copyright
---------

Copyright |copy| 2015 HM Government (Ministry of Justice Digital Services). See
LICENSE for further details.

.. |copy| unicode:: 0xA9 .. copyright symbol
