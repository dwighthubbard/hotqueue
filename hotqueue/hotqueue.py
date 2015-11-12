# -*- coding: utf-8 -*-

"""HotQueue is a Python library that allows you to use Redis as a message queue
within your Python programs.
"""
from __future__ import print_function
from functools import wraps
try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle

try:
    from redislite import Redis
except ImportError:  # pragma: no cover
    from redis import Redis


def key_for_name(name):
    """Return the key name used to store the given queue name in Redis."""
    return 'hotqueue:%s' % name


class HotQueue(object):
    """Simple FIFO message queue stored in a Redis list. Example:

    >>> from hotqueue import HotQueue
    >>> queue = HotQueue("myqueue", host="localhost", port=6379, db=0)

    :param name: name of the queue
    :param serializer: the class or module to serialize msgs with, must have
        methods or functions named ``dumps`` and ``loads``,
        `pickle <http://docs.python.org/library/pickle.html>`_ is the default,
        use ``None`` to store messages in plain text (suitable for strings,
        integers, etc)
    :param: redis: Optional redis connection object
    :param kwargs: additional kwargs to pass to :class:`Redis`, most commonly
        :attr:`host`, :attr:`port`, :attr:`db`
    """

    def __init__(
            self, name, serializer=pickle, redis=None, max_queue_length=None,
            **kwargs
    ):
        self.name = name
        self.serializer = serializer
        self.max_queue_length = max_queue_length
        if redis:
            self.__redis = redis
        else:
            self.__redis = Redis(**kwargs)

    def __len__(self):
        return self.__redis.llen(self.key)

    @property
    def key(self):
        """Return the key name used to store this queue in Redis."""
        return key_for_name(self.name)

    def clear(self):
        """Clear the queue of all messages, deleting the Redis key."""
        self.__redis.delete(self.key)

    def consume(self, **kwargs):
        """Return a generator that yields whenever a message is waiting in the
        queue. Will block otherwise. Example:

        >>> queue = HotQueue("example")
        >>> for msg in queue.consume(timeout=1):
        ...     print(msg)
        my message
        another message

        :param kwargs: any arguments that :meth:`~hotqueue.HotQueue.get` can
            accept (:attr:`block` will default to ``True`` if not given)
        """
        kwargs.setdefault('block', True)
        try:
            while True:
                msg = self.get(**kwargs)
                if msg is None:
                    break
                yield msg
        except KeyboardInterrupt:  # pragma: no cover
            print()
            return

    def get(self, block=False, timeout=None):
        """Return a message from the queue. Example:

        >>> queue.get()
        'my message'
        >>> queue.get()
        'another message'

        :param block: whether or not to wait until a msg is available in
            the queue before returning; ``False`` by default
        :param timeout: when using :attr:`block`, if no msg is available
            for :attr:`timeout` in seconds, give up and return ``None``
        """
        if block:
            if timeout is None:
                timeout = 0
            msg = self.__redis.blpop(self.key, timeout=timeout)
            if msg is not None:
                msg = msg[1]
        else:
            msg = self.__redis.lpop(self.key)
        if msg is not None and self.serializer is not None:
            msg = self.serializer.loads(msg)

        if isinstance(msg, bytes):
            msg = msg.decode()

        return msg

    def put(self, *msgs):
        """Put one or more messages onto the queue. Example:

        >>> queue.put("my message")
        >>> queue.put("another message")

        To put messages onto the queue in bulk, which can be significantly
        faster if you have a large number of messages:

        >>> queue.put("my message", "another message", "third message")
        """
        if self.serializer is not None:
            msgs = [self.serializer.dumps(m) for m in msgs]
        self.__redis.rpush(self.key, *msgs)
        if self.max_queue_length:
            self.__redis.ltrim(self.key, 0, int(self.max_queue_length) - 1)

    def worker(self, *args, **kwargs):
        """Decorator for using a function as a queue worker. Example:

        >>> @queue.worker(timeout=1)
        ... def printer(msg):
        ...     print(msg)
        >>> printer()
        my message
        another message

        You can also use it without passing any keyword arguments:

        >>> @queue.worker
        ... def printer(msg):
        ...     print(msg)
        >>> printer()
        my message
        another message

        :param kwargs: any arguments that :meth:`~hotqueue.HotQueue.get` can
            accept (:attr:`block` will default to ``True`` if not given)
        """
        def decorator(worker):
            """
            Worker decorator
            :param worker:
            :return:
            """
            @wraps(worker)
            def wrapper(*args):
                """
                Inner wrapper
                :param args:
                :return:
                """
                for msg in self.consume(**kwargs):
                    worker(*args + (msg,))
            return wrapper
        if args:
            return decorator(*args)
        return decorator
