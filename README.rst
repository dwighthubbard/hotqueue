========
HotQueue
========

.. image:: https://travis-ci.org/dwighthubbard/hotqueue.svg?branch=master
    :target: https://travis-ci.org/dwighthubbard/hotqueue
    
.. image:: https://coveralls.io/repos/dwighthubbard/hotqueue/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/dwighthubbard/hotqueue?branch=master
  
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
