========
HotQueue
========
:Info: HotQueue is a Python library that allows you to use Redis as a message queue within your Python programs.
:Author: Richard Henry (http://github.com/richardhenry)

About HotQueue
==============

HotQueue is a Python library that allows you to use `Redis <http://code.google.com/p/redis/>`_ as a message queue within
your Python programs.

The main advantage of this model is that there is no queue server to run, other than Redis. This is particularly ideal
if you're already using Redis as a datastore elsewhere.

To install it, run::

    pip install -U hotqueue

To run HotQueue without setting up a seperate redis server install HotQueue with the optional support for the redislite
module.  To install it, run::

    pip install -U hotqueue[redislite]

The best place to get started is `the documentation <http://richardhenry.github.com/hotqueue/>`_.

The source code is available on `GitHub <http://github.com/richardhenry/hotqueue>`_.

To get help with HotQueue, use the `HotQueue Users mailing list
<http://groups.google.com/group/hotqueue-users>`_.

Contributing
============
The source is available on `GitHub <http://github.com/richardhenry/hotqueue>`_. To contribute to the project, fork it on
GitHub and send a pull request, all contributions and suggestions are welcome.

Testing
-------
The python tox tool will run the tests in multiple python virtual environments using all supported python interpreters
installed on the computer system running the tests.  To install it, run::

    pip install tox

The tests using the redis module require that a redis-server be running with the default configuration.  If the
redis-server is not running the py27-redis and py34-redis test environments will fail. To run the
tests in using all python interpreters installed on the system using both the redis and redisliste modules run::

    tox

Code Analysis/Linting
---------------------
The tox tool also is configured to run the pylint tool.  To check the code using pylint, run::

    tox -e pylint

Style Check/PEP8
----------------
The code can be checked for compliance with the Python style guide using the pep8 tool.  To do this, run::

    tox -e pep8

Documentation
-------------
To build the package documentation using the tox tool, run::

    tox -e build_docs

The resulting documentation will be in the build/sphinx/html directory.
