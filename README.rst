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

This source code is provided as-is, with no incident response or support levels.
Please log all questions, issues, and feature requests in the Github issue
tracker for this repo, and we'll take a look as soon as we can. If you're
reporting a bug, then it really helps if you can provide the smallest possible
bit of code that reproduces the issue. A failing test is even better!


Contributing
------------

* Check out the latest master to make sure the feature hasn't been implemented
  or the bug fixed
* Check the issue tracker to make sure someone hasn't already requested and/or
  contributed the feature
* Fork the project
* Start a feature/bugfix branch
* Commit and push until you are happy with your contribution
* Make sure your changes are covered by unit tests, so that we don't break it
  unintentionally in the future.
* Please don't mess with version or history.


Copyright
---------

Copyright |copy| 2015 HM Government (Ministry of Justice Digital Services). See
LICENSE for further details.

.. |copy| unicode:: 0xA9 .. copyright symbol
