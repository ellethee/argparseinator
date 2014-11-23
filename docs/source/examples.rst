=============
Some examples
=============

Simple http requests
====================
This simple script uses the functions approach to send simple http requests
to a server.

.. literalinclude:: ../../httprequest.py
    :language: python


Simple http requests subclassing :class:`ArgParseInated` object
===============================================================
Let's do the same thing but subclassing the ArgParseInated object we can
define the shared argument ``url`` and pass an instance of requests.Session
to he our HttpRequest class.

.. literalinclude:: ../../httprequest2.py
    :language: python
    :emphasize-lines: 15, 21, 33, 43 
