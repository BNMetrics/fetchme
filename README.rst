====================================
Fetchme - Safe Command Aliasing Tool
====================================

.. image:: https://travis-ci.org/BNMetrics/fetchme.svg?branch=master
    :target: https://travis-ci.org/BNMetrics/fetchme

.. image:: https://codecov.io/gh/BNMetrics/fetchme/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/BNMetrics/fetchme


What is fetchme?
================
**fetchme** is a cli tool for safe aliasing. This package allows aliasing of long commands without using the default bash aliasing.

**Why use fetchme?**
  - Safe aliasing commands, no more accident in overriding a existing command
  - Easy to use



Installation
============

Make sure python 3.6 is installed on your machine, if not, click `here <https://www.python.org/downloads/>`_ to follow the instructions on installation.


Then install the latest version of fetchme via **pip**:

.. code-block:: bash

    $ pip3 install fetchme


Once you install the package, there will be a configuration file ``.fetchmerc`` generated in your *home directory*,
and this is where you put all your aliases.


Usage & References
==================

Default Commands
----------------

**fetchme** comes with 3 default commands: ``edit``, ``set`` and ``remove``.


edit:
~~~~~

``edit`` command opens up the ``.fetchmerc`` file in an editor. If you have configured your preferred editor in the environment variable ``EDITOR``,
the preferred editor will be launched. The default editor is ``vim`` if the environment variable is not being configured.

**Usage**:

::

    fetchme edit [OPTIONS]


**Example**:

.. code-block:: bash

    $ fetchme edit



set:
~~~~

This command is for setting an alias to a long command.

**Usage**:

::

    fetchme set [OPTIONS] CONTENT


**Example**:

.. code-block:: bash

    $ fetchme set ssh="ssh -i /path/to/my/key/file root@123.43.678.678"


The ``CONTENT`` argument is where you set your alias as key=value pair, it is recommended that you **quote** the command that is
to be aliased, like so in the example.

An additional line will be added to ``.fetchmerc`` file after the ``set`` command is being executed.

.. code-block:: ini

    [fetchme]
    ssh = ssh -i /path/to/my/key/file root@123.43.678.678


**Options**:

--override, -o: *flag*, override an existing alias, this flag must to be past when you
                        need to overriding an existing alias that has already been set.


remove:
~~~~~~~

This command is to remove an existing alias.

**Usage**:

::

    fetchme remove [OPTIONS] NAME


**Example**:

.. code-block:: bash

    $ fetchme remove ssh



The ``NAME`` argument corresponds to an alias that is being set in the ``.fetchmerc`` file.



Executing Aliased Commands
--------------------------

Once you have ``set`` the alias to your command, you can execute your command by directing calling it with fetchme.

**Usage**:

::

    fetchme ALIAS [OPTIONS]


**Example**:

.. code-block:: bash

    $ fetchme ssh


To see the original *unaliased* command, you can use the ``-h`` flag to bring up the descriptions.