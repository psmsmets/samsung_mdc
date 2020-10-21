***********
samsung_mdc
***********

Python3 implementation of the Samsung Multiple Display Control Protocol via
TCP/IP as documented in the Smart Signage User Manual (Common Use)
LFDCOMNEN-01_Common-use_2018_Eng_20190329.0

A fork of Damien Plenard's `python-mdc <https://git.vpgrp.io/noc/python-mdc>`_.

Features
========

Provides a **class** ``MultipleDisplayControl`` to initiate the Samsung 
Multiple Display Control object as well as a simple **command-line-tool** for 
direct control via a terminal.

Usage
=====

Object
------

Create a Samsung Multiple Display Control object

.. code-block:: python

    >>> from samsung_mdc import MultipleDisplayControl
    >>> mdc = MultipleDisplayControl(192.168.1.100)
    >>> print(mdc)
    MDC #0xfe @192.168.1.100:1515

By default no connection is initiated by the socket

.. code-block:: python

    >>> print(mdc.connected)
    False

Connect to the remote socket

.. code-block:: python

    >>> mdc.connect()
    >>> print(mdc.connected)
    True

Control the TV

.. code-block:: python

    >>> mdc.power  # print power status
    False
    >>> mdc.power = !mdc.power  # toggle power
    >>> mdc.get_power()  # print new power status
    1
    >>> mdc.set_power(False)  # off

Close the connection

.. code-block:: python

    >>> mdc.close()
    >>> print(mdc.connected)
    False

Using the ``with`` statement the connection is initiated and terminated
automatically

.. code-block:: python

    with MultipleDisplayControl(192.168.1.100) as mdc:
        mdc.power = True
        mdc.source = 'hdmi2'
        mdc.safety_lock = True


Command-line-tool
-----------------

In the terminal execute

.. code-block:: console

    >>> samsung_mdc --help

to show this help message and exit

.. code-block:: console

    usage: samsung_mdc [-h] [-p ..] [-i ..] [--version]
                       host command [data [data ...]]

    Samsung Multiple Display Control Protocol via TCP/IP

    positional arguments:
      host              Remote TV ipv4-address
      command           Control command name
      data              Data argument(s) for the set control command
                        (controlling). If empty (default), set get control command
                        is returned (viewing control state).

    optional arguments:
      -h, --help        show this help message and exit
      -p .., --port ..  Remote TV port
      -i .., --id ..    Remote TV id
      --version         Print samsung_mdc version and exit


Installation
============

Create a clone, or copy of the samsung_mdc repository

.. code-block:: console

    git clone https://gitlab.com/psmsmets/samsung_mdc.git

Run ``git pull`` to update the local repository to this master repository.


Install samsung_mdc via ``pip``:

.. code-block:: console

   cd samsung_mdc
   pip install -e .


Required are Python version 3.6 or higher.


License information
===================

Licensed under the GNU GPLv3 License. See the ``LICENSE``- and ``NOTICE``-files
or the documentation for more information.
