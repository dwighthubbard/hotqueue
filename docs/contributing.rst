Contributing
============
The source is available on `GitHub <http://github.com/dwighthubbard/hotqueue>`_. To contribute to the project, fork it
on GitHub, run the tests, code analysis and style checks using the instructions below.  Then send a pull request, all
contributions and suggestions are welcome.

This project is a fork of the source available on `GitHub <http://github.com/richardhenry/hotqueue>`_.

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
The tox tool also is configured with a test envioronment to run the pylint tool.  To check the code for common
problems using pylint, run::

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
