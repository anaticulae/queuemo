strategy
========

This document describes the connect process and the connection between
the different modules.

.. note:: think about document name

connection process
------------------

naming
~~~~~~

* Process: A process is a algorithm which transform data and has in- and out-
  ports.

* Port: A port is a connection which is flown by data.

* Outputdata: The output data is processed by the process. The naming of
  the data fits into the pattern:

    .. code-block:: none

        process__featureA_datum_a
        process__featureA_datum_b
        process__featureB_datum_a

* Datapool: A datapool is represented by one or more folder. The folder
  contains different data. The folder is named by the process itself.
