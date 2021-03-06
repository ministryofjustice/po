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

    ./manage.py runserver 0.0.0.0:8000

Access the server at http://localhost:8000/

And the admin at http://localhost:8000/admin/


Configuration
-------------

The Django settings file is located in `po/settings/base.py`.

.. note::
  To avoid committing sensitive data such as passwords and auth tokens
  to Github, you can put your development settings in `po/settings/local.py`,
  which is ignored by Git.

The main settings you might want to change are taken from the following
environment variables:

* **GITHUB_TOKEN** - a Github OAuth token allowing read access to repositories
* **ZENDESK_URL** - the URL of a Zendesk subdomain (eg:
  https://ministryofjustice.zendesk.com/)
* **ZENDESK_USERNAME** - the username of the Zendesk API user (usually an email
  address)
* **ZENDESK_TOKEN** - a Zendesk API OAuth token

Usage
-----

Pushing APT dependency information for a deployment to the API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To automatically submit APT package dependencies for an app on deployment by
Jenkins (or other CI system), a build step needs to call the
`scripts/post-dependencies.sh` script.

This script will query `dpkg` for a list of installed packages, generate a JSON
payload and POST it to the Platform Overseer API.

The following environment variables need to be set:

* **PROJECT** - the name of the project/app
* **APP_BUILD_TAG** - the name of the build (tries BUILD_TAG if not set)
* **ENV** - the name of the deployment environment, eg: staging

Pushing healthcheck.json and ping.json existence to the API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To check for the healthcheck.json and ping.json APIs in a deployment, add a
build step to the Jenkins (or other CI) job which calls the
`scripts/push-healthcheck-and-ping.sh` script.

This script will test that HTTP GET requests to the /healthcheck.json and
/ping.json URLs return a 200 status code, and send that in a JSON payload to the
Platforms Overseer API.

Pulling Ruby dependency information for all repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To scan all ministryofjustice organisation repositories (public and private) for
Ruby dependency information, run the following command on the PO server::

    python manage.py spider_github

The script will gather metadata about every repository, including language
usage, ruby gem dependencies and existence of Ruby or Python unit tests.

Pulling recent incident count from Zendesk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get the number of incidents reported on products in the last two weeks (one
of the IRAT checklist requirements is that there were less than two incidents in
the last two weeks), run the following command::

    python manage.py check_incidents

This command needs to be run on a regular interval to pick up new incidents. The
PO server should have cron job that runs this command every day (or similar).


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
