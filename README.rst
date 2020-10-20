***********
samsung_mdc
***********

Implementation of the Samsung Multiple Display Control Protocol via TCP/IP
in Python3 as documented in the Smart Signage User Manual (Common Use)
LFDCOMNEN-01_Common-use_2018_Eng_20190329.0

A fork of Damien PLENARD's `python-mdc <https://git.vpgrp.io/noc/python-mdc>`_.

Features
========

Provides a class ``MultipleDisplayControl`` to initiate the Samsung Multiple
Display Control object as well as a simple command-line-tool for direct control
via a terminal.


Installation
============

Create a clone, or copy of the xcorr repository

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
