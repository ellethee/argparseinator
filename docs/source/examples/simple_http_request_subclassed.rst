Simple HTTP requests sub-classing :class:`ArgParseInated` object
================================================================
Let's do the same thing but by inheriting the class from :class:`ArgParseInated`.
We can define the shared argument ``url`` and pass an instance of requests.Session
to our HttpRequest class.

Download :download:`this example script <../../../examples/httprequest2.py>`.

.. literalinclude:: ../../../examples/httprequest2.py
    :language: python
    :caption: httprequest2.py
    :name: httprequest2.py
.. :emphasize-lines: 15, 21, 33, 43 .
