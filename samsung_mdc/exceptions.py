r"""

:mod:`exceptions` -- Exceptions
======================================

Useful exceptions for the Samsung Multiple Display Control

"""


class SourceNotExist(Exception):
    """Source do not exist."""

    pass


class InvalidVolume(Exception):
    """Invalid volume value."""

    pass


class InvalidVideoWallMode(Exception):
    """Invalid volume value."""

    pass


class VideoWallNotSupported(Exception):
    """Video Wall not supported."""

    pass
