# -*- coding: utf-8 -*-
"""
samsung_mdc

Implementation of the Samsung Multiple Display Control Protocol via TCP/IP
in Python3 as documented in the Smart Signage User Manual (Common Use)
LFDCOMNEN-01_Common-use_2018_Eng_20190329.0

Based on the original pip project by Damien PLENARD
https://git.vpgrp.io/noc/python-mdc

:author:
    Pieter Smets (mail@pietersmets.be)

:copyright:
    Pieter Smets (mail@pietersmets.be)

:license:
    This code is distributed under the terms of the
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


# Import samsung_mdc modules
from samsung_mdc import util, mdc

# Import MDC class
from samsung_mdc.mdc import MultipleDisplayControl

# Make only a selection available to __all__ to not clutter the namespace
# Maybe also to discourage the use of `from samsung_mdc import *`.
__all__ = ['util', 'mdc', 'MultipleDisplayControl']

# Version
try:
    # - Released versions just tags:       1.10.0
    # - GitHub commits add .dev#+hash:     1.10.1.dev3+g973038c
    # - Uncom. changes add timestamp: 1.10.1.dev3+g973038c.d20191022
    from samsung_mdc.version import version as __version__
except ImportError:
    # If it was not installed, then we don't know the version.
    # We could throw a warning here, but this case *should* be
    # rare. empymod should be installed properly!
    from datetime import datetime
    __version__ = 'unknown-'+datetime.today().strftime('%Y%m%d')
