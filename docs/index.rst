========
HotQueue
========

HotQueue is a Python library that allows you to use `Redis <http://code.google.com/p/redis/>`_ as a FIFO message queue within your Python programs. Using HotQueue looks a little bit like this…

Establishing a queue:

    >>> queue = HotQueue("myqueue")

Putting messages onto the queue:

    >>> queue.put("my message")
    >>> queue.put({'name': "Richard Henry", 'eyes': "blue"})

Getting messages off the queue:

    >>> queue.get()
    "my message"
    >>> queue.get()
    {'name': 'Richard Henry', 'eyes': 'blue'}

Iterating over a queue indefinitely, waiting if nothing is available:

    >>> for item in queue.consume():
    ...     print item

More advanced features that make it easy to work with queues are available. To go deeper, you should read the :doc:`tutorial`.

The main advantage of the HotQueue model is that there is no queue server to run since the `redislite` module will
handle starting/stopping a redis server automatically as needed. Plus, Redis is really fast!

Installation
============

To install it, run:

.. code-block:: console

    pip install -U redislite-hotqueue

It also works with ``easy_install``, if that's your jam. You can `download versioned packages directly from PyPI <http://pypi.python.org/pypi/hotqueue>`_.

The source code is available on `GitHub <http://github.com/dwighthubbard/hotqueue>`_ and is a fork of the
code available at`GitHub <http://github.com/richardhenry/hotqueue>`_.

To get help with HotQueue, use the `HotQueue Users mailing list <http://groups.google.com/group/hotqueue-users>`_.

Documentation
=============

.. toctree::
   :maxdepth: 2
   
   tutorial
   apireference
   contributing
   changelog

Requirements
============

- Python 2.7+ (tested on versions 2.7.10, 3.4.3, and pyp 2.6.1)
- `redislite <http://redis.io/>`_ 1.0.254+
