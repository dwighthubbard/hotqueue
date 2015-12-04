=================
HotQueue Tutorial
=================

A HotQueue is a simple FIFO queue that maps to a list key in Redis. The following is a brief introduction explaining how you can use HotQueue in practice with a simple example. 

Connecting to Redis
===================

Creating a queue is as simple as creating a :class:`~hotqueue.HotQueue` instance:

    >>> from hotqueue import HotQueue
    >>> queue = HotQueue("myqueue", dbfilename="/tmp/redis.rdb")

In this example, the queue will be stored as a Redis list named ``hotqueue:myqueue``, on the `redislite` server.
The :attr:`dbfilename` argument is optional; if none are given the `redislite` default setings will be used.

Putting Items Onto the Queue
============================

Then you may have one (or many) Python programs pushing to the queue using :meth:`hotqueue.HotQueue.put`:

    >>> queue.put(4)
    >>> queue.put(5)

You can push more than one item onto the queue at once:

    >>> queue.put(6, "my message", 7)

You can safely push **any Python object** that can be `pickled <http://docs.python.org/library/pickle.html>`_. Let's use Python's built-in ``Decimal`` as an example:

    >>> from decimal import Decimal
    >>> queue.put(Decimal('1.4'))

Getting Items Off the Queue
===========================

You can then pull items off the queue using :meth:`hotqueue.HotQueue.get`. You would usually do this in another Python program, but you can do it wherever you like.

    >>> queue.get()
    4
    >>> queue.get()
    5
    >>> queue.get()
    6
    >>> queue.get()
    'my message'
    >>> queue.get()
    7
    >>> dec = queue.get()
    >>> dec
    Decimal('1.4')
    >>> dec + Decimal('0.3')
    Decimal('1.7')

Consuming the Queue
===================

A better way to pull items off the queue is to use :meth:`hotqueue.HotQueue.consume`, which returns a generator that yields whenever an item is on the queue and blocks otherwise. Here's an example:

    >>> for item in queue.consume():
    ...     print item

If you push to the queue using :meth:`hotqueue.HotQueue.put` in another Python program, you will see this program print the message then wait indefinitely for another. Replace the ``print`` statement with something more interesting, like saving a record to a database, and you've created an asynchronous task.

Writing a Queue Worker
======================

An `even better` way to pull items off the queue is to use the :meth:`hotqueue.HotQueue.worker` decorator. Using this decorator is like wrapping the decorated function in a :meth:`hotqueue.HotQueue.consume` loop. Here's an example::

    from hotqueue import HotQueue
    
    queue = HotQueue("myqueue", dbfilename="/tmp/redis.rdb")
    
    @queue.worker
    def square(num):
        print num * num

Then run the function:

    >>> square()

It will wait indefinitely and print the square of any integers it pulls off the queue. Try pushing some integers to the queue in another Python program:

    >>> queue.put(2, 3, 4)

To distribute the work, run a second instance of ``square()``. You now have two queue workers. You can run as many workers as you like, and no two workers will ever receive the same message.

To run and manage your worker processes, you could use something like `Supervisord <http://supervisord.org/>`_.

Custom Serialization (JSON, etc)
================================

If you don't want to use the `pickle <http://docs.python.org/library/pickle.html>`_ serializer, you can specify any other class or module that has the same API.

To serialize your data as JSON, you can use the `json <http://docs.python.org/library/json.html>`_ module. Here's an example:

    >>> import json
    >>> from hotqueue import HotQueue
    >>> queue = HotQueue("myqueue", serializer=json, dbfilename="/tmp/redis.rdb")
    >>> queue.put({'name': "Richard Henry", 'eyes': "blue"})
    >>> queue.get()
    {'name': 'Richard Henry', 'eyes': 'blue'}

JSON serialization is particularly useful if you will be accessing this Redis list from programming languages other than Python, or want to ensure that your queue can be read between Python versions.

If you can, you should use `simplejson <http://pypi.python.org/pypi/simplejson/>`_ instead of `json <http://docs.python.org/library/json.html>`_. It's updated more frequently, and can be significantly faster than the module that ships with the standard library. You should take a look at `jsonpickle <http://jsonpickle.github.com/>`_ if you want to serialize more complex Python data structures to JSON.

Feel free to write your own serializer. Here's a dummy class to give you an idea of the API required::

    class DummySerializer(object):
        """Serialization class that doesn't do anything. Fill in the dumps and
        loads methods with your own code.
        """
        @staticmethod
        def dumps(obj):
            """Serialize the given object."""
            return obj
        @staticmethod
        def loads(data):
            """De-serialize the given data back to an object."""
            return data

Disabling Serialization
=======================

If your messages can be converted to plain text without losing any information, then you can get some performance gains by not doing any serialization at all. This is ideal if you're queueing strings, CSV data, and so on.

To disable serialization, pass ``None`` to the serializer argument:

    >>> queue = HotQueue("myqueue", serializer=None)
    >>> queue.put("my,csv,data")
    >>> queue.get()
    "my,csv,data"

Monitoring
==========

The following software is available for monitoring your HotQueue queue instances:

- `HotWatch <https://github.com/richardhenry/hotwatch>`_: Command line utility for monitoring the status of HotQueue queue instances.
