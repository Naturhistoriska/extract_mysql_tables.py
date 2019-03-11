extract_mysql_tables.py
=======================

``extract_mysql_tables.py`` is a small command-line utility for extracting 
data from a MySQL database and writing each table to a file with 
tab-separated values. Each file will be named after the table, suffixed 
with ".tsv".

The code has been tested with Python 3.6.

Source repository: `<https://github.com/naturhistoriska/extract_mysql_tables.py>`_

--------------------------------

.. contents:: Table of contents
   :local:
   :backlinks: none


Prerequisites
-------------

* Python 3
* The Python library `PyMySQL <https://pymysql.readthedocs.io/en/latest/>`_

An easy way to get Python working on your computer is to install the free
`Anaconda distribution <http://anaconda.com/download)>`_.


Installation
------------

The project is hosted at `<https://github.com/naturhistoriska/extract_mysql_tables.py>`
and can be downloaded using git:

.. code-block::

    $ git clone https://github.com/naturhistoriska/extract_mysql_tables.py


Usage
-----

.. code-block::

    ./extract_mysql_tables.py --help
    usage: extract_mysql_tables.py [-h] [-V] [-u USER] [-p PASSWORD] [--host HOST]
                                   [--table-type {1,2,3}] [-o DIR]
                                   database [table-file]

    Command-line utility for exporting tables from a MySQL database to files in
    tab-separated values (TSV) format.

    positional arguments:
      database              database name
      table-file            file with table names separated by newline characters
                            (if missing, all tables will be exported)

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -u USER, --user USER  MySQL user (default: "root")
      -p PASSWORD, --password PASSWORD
                            MySQL password
      --host HOST           database host (default: "localhost")
      --table-type {1,2,3}  Table type to include in export: 1=BASE TABLE; 2=VIEW;
                            3=SYSTEM VIEW (i.e. INFORMATION_SCHEMA table). The
                            table type will be ignored if there is a file provided
                            with table names.
      -o DIR, --output-dir DIR
                            path to the output directory (default: current
                            directory)



Python code style conventions
-----------------------------

The code follow style conventions in `PEP 8
<https://www.python.org/dev/peps/pep-0008/>`_, which can be checked
with `pycodestyle <http://pycodestyle.pycqa.org>`_:

.. code-block::

    $ pycodestyle extract_mysql_tables.py


License
-------

``extract_mysql_tables.py`` is distributed under the 
`MIT license <https://opensource.org/licenses/MIT>`_.


Author and maintainer
---------------------

Markus Englund, markus.englund@nrm.se
