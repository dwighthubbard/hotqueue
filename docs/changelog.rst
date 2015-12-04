=========
Changelog
=========
Changes in v1.3.0
=================
- Add support for `redislite` to allow operation without installing a redis server.
- Implement CI/CD pipeline to automate the build and testing against multiple python versions.

Changes in v0.2.7
=================
- ``serializer`` argument of ``HotQueue.put`` method now supports ``None`` for plain text serialization
- If multiple messages are passed to ``HotQueue.put`` they will be sent in the same command for a significant performance benefit

Changes in v0.2.6
=================
- Removed the ``HotQueue.__repr__`` method as it is no longer supported

Changes in v0.2.5
=================
- Fixed a bug in v0.2.4 that prevented install in some environments

Changes in v0.2.4
=================
- ``HotQueue.worker`` decorator method can now be used to decorate a class method

Changes in v0.2.3
=================
- Added support for custom serialization (JSON, etc)

Changes in v0.2.2
=================
- Added ``key_for_name`` function

Changes in v0.2.1
=================
- ``HotQueue.worker`` decorator method can now be used without any keyword arguments

Changes in v0.2.0
=================
- Renamed ``HotQueue.dequeue`` method to ``get``
- Renamed ``HotQueue.enqueue`` method to ``put``
- Added ``HotQueue.worker`` decorator method
- ``HotQueue.get`` method now supports block and timeout arguments
- Added test suite

Changes in v0.1.0
=================
- Initial release
