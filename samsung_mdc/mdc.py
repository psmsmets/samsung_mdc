r"""

:mod:`mdc` -- Multiple Display Control
======================================

Samsung Multiple Display Control object

"""

# mandatory imports
import socket

# relative imports
from .util import is_valid_ipv4_address, verify_key_value


__all__ = ['MultipleDisplayControl']


_commands = {
    0x11: 'Power',
    0x12: 'Volume',
    0x13: 'Mute',
    0x14: 'Input_source',
    0x19: 'Screen_size',
    0x5C: 'Video_wall_mode',
    0x5D: 'Satefy_Lock',
    0x84: 'Video_Wall_On',
    0x89: 'Video_Wall_User',
}

_input_sources_set = {
    0x0C: 'Input source',
    0x18: 'DVI',
    0x20: 'MagicInfo',
    0x21: 'HDMI1',
    0x23: 'HDMI2',
    0x25: 'DisplayPort'
}

_input_sources_get = {
    **_input_sources_set,
    0x1F: 'DVI_video',
    0x22: 'HDMI1_PC',
    0x24: 'HDMI2_PC',
}

_video_wall_modes = {
    0x00: 'Natural',
    0x01: 'Full',
}


class MultipleDisplayControl(object):
    """
    """

    __slots__ = (
        "__host",
        "__port",
        "__id",
        "__attrs",
        "__socket",
        "__connected",
    )

    def __init__(self, host: str = None, port: int = None,
                 id: int = None, attrs: dict = None, **kwargs):
        """Construct a Samsung Multiple Display Control (MDC) object.

        Parameters:
        -----------
        host : `string`
            Host ipv4-address.

        port : `int`, optional
            Connection port [0, 65535]. Defaults to 1515.

        id : `int`
            Display id [0, 255]. Defaults to 254 for globing.

        attrs : `dict`
            Dictionary of global attributes on this object

        **kwargs :
            Any kwargs are added to the global attributes.

        Example:
        --------

        Create an MDC object and connect to the remote socket:

        >>> mdc = MultipleDisplayControl(192.168.1.100)
        >>> mdc.connect()
        >>> mdc.power  # print power status
        >>> mdc.power = !mdc.power  # toggle power
        >>> mdc.power  # print new power status
        >>> mdc.close()

        Or using the `with` statement. Now the connection is initiated and
        terminated automatically:

        >>> with MultipleDisplayControl(192.168.1.100) as mdc:
                print(mdc)
                mdc.power = True
                mdc.source = 'hdmi2'
                mdc.safety_lock = True
        """
        self.__connected = False
        self.__attrs = dict(attrs) if attrs is not None else None
        if kwargs:
            self.attrs = {**self.attrs, **kwargs}

        self.__id = id or 254
        if not isinstance(self.__id, int):
            raise TypeError('mdc_id should be of type integer')
        if self.__id < 0 or self.__id > 255:
            raise ValueError('mdc_id should be within [0, 255]')

        self.__host = host
        if not isinstance(self.__host, str):
            raise TypeError('host should be of type string')
        if not is_valid_ipv4_address(self.__host):
            raise ValueError('host is not a valid ipv4 address')

        self.__port = port or 1515
        if not isinstance(self.__port, int):
            raise TypeError('port should be of type integer')
        if self.__port < 0 or self.__port > 65535:
            raise ValueError('port should be within [0, 65535]')

        self.__socket = socket.socket(family=socket.AF_INET,
                                      type=socket.SOCK_STREAM)
        return

    def __del__(self):
        """Destruct the MDC object.
        """
        if self.connected:
            self.close()

    def __str__(self):
        """Printable string representation of an MDC object.
        """
        return 'MDC #{} @{}:{}'.format(
            hex(self.id), self.host, self.port
        )

    def __repr__(self):
        """String representation of an MDC object.
        """
        return 'MultipleDisplayControl(host={}, port={}, mdc_id={})'.format(
            self.host, self.port, hex(self.id)
        )

    def __enter__(self):
        """Enter an MDC object.
        """
        if not self.connected:
            self.connect()
        return self

    def __exit__(self, *args):
        """Exit the MDC object.
        """
        self.__del__()

    def __eq__(self, other):
        """Check equality of an MDC object.
        """
        if not isinstance(other, MultipleDisplayControl):
            return False
        return (self.host == other.host and
                self.port == other.port and
                self.id == other.id)

    def __getattr__(self, name: str):
        if name not in {"__dict__", "__setstate__"}:
            # this avoids an infinite loop when pickle looks for the
            # __setstate__ attribute before the object is initialized
            if name in self.attrs:
                return self.attrs[name]
        raise AttributeError(
            "{!r} object has no attribute {!r}".format(
                type(self).__name__, name
            )
        )

    def __getitem__(self, name: str):
        if name not in {"__dict__", "__setstate__"}:
            # this avoids an infinite loop when pickle looks for the
            # __setstate__ attribute before the object is initialized
            if name in self.attrs:
                return self.attrs[name]
            elif name in [slot[2:] for slot in self.__slots__]:
                return eval(f'self.{name}')
        raise AttributeError(
            "{!r} object has no attribute {!r}".format(
                type(self).__name__, name
            )
        )

    def __setitem__(self, name, value):
        raise NotImplementedError(
            "cannot set item %r on a %r object."
            % (name, type(self).__name__)
        )

    def __setattr__(self, name, value):
        """Objects with ``__slots__`` raise AttributeError if you try setting
        an undeclared attribute. This is desirable, but the error message could
        use some improvement.
        """
        try:
            object.__setattr__(self, name, value)
        except AttributeError as e:
            # Don't accidentally shadow custom AttributeErrors, e.g.
            # DataArray.dims.setter
            if str(e) != "{!r} object has no attribute {!r}".format(
                type(self).__name__, name
            ):
                raise
            raise AttributeError(
                "cannot set attribute %r on a %r object. Use the `set_attr()` "
                "mutator (e.g., `mdc.set_attr('name', ...)` instead of "
                "assigning variables."
                % (name, type(self).__name__)
            ) from e

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def id(self):
        return self.__id

    @property
    def connected(self):
        return self.__connected

    @property
    def _socket(self):
        return self.__socket

    @property
    def attrs(self):
        """Dictionary of global attributes on this object"""
        if self.__attrs is None:
            self.__attrs = {}
        return self.__attrs

    @attrs.setter
    def attrs(self, value):
        self.__attrs = dict(value)

    def set_attr(self, name: str, value):
        """Set a global attribute on this object
        """
        self.__attrs[name] = value

    def get_attr(self, name: str):
        """Get a global attribute from this object
        """
        return self.attrs[name]

    def connect(self):
        """Connect the socket to the remote TV
        """
        try:
            self.__socket.connect((self.host, self.port))
            self.__connected = True
        except socket.timeout:
            self.__connected = False

    def close(self):
        """Close the socket to the remote TV
        """
        self.__socket.close()
        self.__connected = False

    def detach(self):
        """Detach the socket to the remote TV
        """
        self.__socket.detach()
        self.__connected = False

    def _get(self, command):
        """Private helper to construct a view control state command
        """
        command_id = verify_key_value(command, _commands, 'command')
        return [0xAA, command_id, self.id, 0]

    def _set(self, command, *args):
        """Private helper to construct a controlling command
        """
        command_id = verify_key_value(command, _commands, 'command')

        if not all(isinstance(arg, (bool, int)) for arg in args):
            raise TypeError('args should be either a bool or integer')

        args = [abs(int(arg)) % 256 for arg in args]  # limit to uint8
        return [0xAA, command_id, self.id, len(args)] + list(args)

    def _send(self, command):
        """Private helper to send a command to the remote TV
        """
        if not self.connected:
            raise RuntimeError('socket is not connected')
        checksum = sum(command[1:]) % 256
        command.append(checksum)
        return self._socket.send(bytes(command))

    def _recv(self):
        """Private helper to receive data from the remote TV
        """
        if not self.connected:
            raise RuntimeError('socket is not connected')
        return self._socket.recv(2)

    @property
    def power(self):
        """View/control the power state (0x11):
        """
        return bool(self.get_power())

    @power.setter
    def power(self, value):
        self.set_power(value)

    def get_power(self):
        """View the power state (0x11).

        Returns:
        --------
        value: `bool`
        """

        self._send(self._get(0x11))
        return self._recv()

    def set_power(self, value):
        """Control the power state (0x11).

        Parameters:
        -----------
        state: `bool` or `int`
        """
        if not isinstance(value, (bool, int)):
            raise TypeError('power state should be of type bool or int')
        self._send(self._set(0x11, bool(value)))

    @property
    def volume(self):
        """View/control the volume (0x12).
        """
        return self.get_volume()

    @volume.setter
    def volume(self, value: int):
        self.set_volume(value)

    def get_volume(self):
        """View the volume (0x12).

        Returns:
        --------
        value: `int`
            Get volume [0, 100].
        """
        self._send(self._get(0x12))
        return self._recv()

    def set_volume(self, value: int):
        """Control the volume (0x12).

        Parameters:
        -----------
        value: `int`
            Set volume [0, 100].
        """
        if not isinstance(value, int):
            raise TypeError('volume should be of type integer')
        if value < 0 or value > 100:
            raise ValueError('volume should be within [0, 100]')
        self._send(self._set(0x12, value))

    @property
    def mute(self):
        """View/control mute state (0x13):
        """
        return bool(self.get_mute())

    @mute.setter
    def mute(self, value: bool):
        self.set_mute(value)

    def get_mute(self):
        """View the mute state (0x13).

        Returns:
        --------
        value: `bool`
        """
        self._send(self._get(0x13))
        return self._recv()

    def set_mute(self, value):
        """Control the mute state (0x13).

        Parameters:
        -----------
        value: `bool` or `int`
        """
        if not isinstance(value, (bool, int)):
            raise TypeError('mute state should be of type bool or int')
        self._send(self._set(0x13, bool(value)))

    @property
    def source(self):
        """View/control source (0x14).
        """
        _input_sources_get(self.get_source())

    @source.setter
    def source(self, value):
        self.set_source()

    def get_source(self):
        """View the source (0x14).

        Returns:
        --------
        value: `string`
            Returns the input source id
        """
        self._send(self._get(0x14))
        return self._recv()

    def set_source(self, value):
        """Control the source (0x14).

        Parameters:
        -----------
        value: `int` or `string`
            Set the source according to the integer/hexadecimal value or name:
                - 0x0C: Input source
                - 0x18: DVI
                - 0x20: MagicInfo
                - 0x21: HDMI1
                - 0x23: HDMI2
                - 0x25: DisplayPort
        """
        value = verify_key_value(value, _input_sources_set, 'source')
        return self._send(self._set(0x14, value))

    @property
    def screen_size(self):
        """View/control screen size (0x19).
        """
        return self.get_screen_size()

    @screen_size.setter
    def screen_size(self, value: int):
        self.set_screen_size(value)

    def get_screen_size(self):
        """View the screen size (0x19).

        Returns:
        --------
        value: `int`
            Get volume [0, 100].
        """
        self._send(self._get(0x19))
        return self._recv()

    def set_screen_size(self, value: int):
        """Control the screen size (0x19).

        Parameters:
        -----------
        value: `int`
            Set screen size [0, 255].
        """
        if not isinstance(value, int):
            raise TypeError('screen size should be of type integer')
        if value < 0 or value > 255:
            raise ValueError('screen size should be within [0, 255]')
        self._send(self._set(0x19, value))

    @property
    def video_wall_mode(self):
        """View/toggle video wall mode (0x5C).
        """
        return _video_wall_modes[self._recv()]

    @video_wall_mode.setter
    def video_wall_mode(self, value):
        """
        """
        self.set_video_wall_mode(value)

    def get_video_wall_mode(self):
        """View the video wall mode (0x5C).

        Returns:
        --------
        value: `int`
        """
        self._send(self._get(0x5C))
        return self._recv()

    def set_video_wall_mode(self, value):
        """Control the video wall mode (0x5C).

        Parameters:
        -----------
        value: `int` or `str`
            Set video wall mode:
                - 0: Natural
                - 1: Full
        """
        value = verify_key_value(value, _video_wall_modes, 'video_wall_mode')
        self._send(self._set(0x5C, value))

    @property
    def safety_lock(self):
        """View/control safety lock state (0x5D).
        """
        return bool(self.get_safety_lock())

    @safety_lock.setter
    def safety_lock(self, value):
        """
        """
        self.get_safety_lock(value)

    def get_safety_lock(self):
        """View the safety lock state (0x5D).

        Returns:
        --------
        value: `bool`
        """
        self._send(self._get(0x5D))
        return self._recv()

    def set_safety_lock(self, value):
        """Control the safety lock state (0x5D).

        Parameters:
        -----------
        value: `bool` or `int`
        """
        if not isinstance(value, (bool, int)):
            raise TypeError('safety lock state should be of type bool or int')
        self._send(self._set(0x5D, bool(value)))

    @property
    def video_wall_on(self):
        """View/control video wall on state.
        """
        return bool(self.get_video_wall_on())

    @video_wall_on.setter
    def video_wall_on(self, value: bool):
        self.set_video_wall_on(value)

    def get_video_wall_on(self):
        """View the video wall on state (0x5D).

        Returns:
        --------
        value: `bool`
        """
        self._send(self._get(0x84))
        return self._recv()

    def set_video_wall_on(self, value):
        """Control the video wall on state (0x84).

        Parameters:
        -----------
        value: `bool` or `int`
        """
        if not isinstance(value, (bool, int)):
            raise TypeError('video wall on should be of type bool or int')
        self._send(self._set(0x84, bool(value)))

    @property
    def video_wall_user(self):
        """View/set video wall user control.

        Parameters:
        -----------
        values: (col, row, pos)
            - col: `int`
                 Video wall columns (horizontal, max 15).
                 If 0, video wall is disabled.
            - row: `int`
                Video wall rows (vertical, max 15).
                If 0, video wall is disabled.
            - pos: `int`
                Video wall position code (starting first row top/left)
                Maximum number of positions/screens is limited to 100.
        """
        return self.get_video_wall_user()

    @video_wall_user.setter
    def video_wall_user(self, values: tuple):
        """
        """
        col, row, pos = values
        self.set_video_wall_user(col, row, pos)

    def get_video_wall_user(self):
        """Set video wall user control.

        Return:
        -------
        col: `int`
            Set video wall columns (horizontal, max 15).
            If 0, video wall is disabled.
        row: `int`
            Set video wall rows (vertical, max 15).
            If 0, video wall is disabled.
        pos: `int`
            Set video wall position code (starting first row top/left)
            [1, ``col`` * ``row`` <= 100].
            Maximum number of positions/screens is limited to 100.
        """
        self._send(self._get(0x89))
        return self._recv()

    def set_video_wall_user(self, col: int, row: int = None, pos: int = None):
        """Set video wall user control.

        Parameters:
        -----------
        col: `int`
            Set video wall columns (horizontal, max 15).
            If 0, video wall is disabled.
        row: `int`
            Set video wall rows (vertical, max 15).
            If 0, video wall is disabled.
        pos: `int`
            Set video wall position code (starting first row top/left)
            [1, ``col`` * ``row`` <= 100].
            Maximum number of positions/screens is limited to 100.
        """
        row = row or col
        if not isinstance(col, int) or not isinstance(row, int):
            raise TypeError('col and row should be of type integer')
        screens = col * row
        if col < 0 or col > 15 or row < 0 or row > 15 or screens > 100:
            raise ValueError('col and row should be within [0, 15] '
                             'with total number of screens <= 100')
        if screens == 0:
            wall_div = '0x00'
            wall_sno = '0x00'
        else:
            wall_div = f'0x{hex(row)[-1]}{hex(col)[-1]}'
            if not isinstance(pos, int):
                raise TypeError('pos should be of type integer')
            if pos < 1 or pos > screens:
                raise ValueError(f'pos should be within [1, {screens}]')
            wall_sno = int(pos)

        self._send(self._set(0x89, wall_div, wall_sno))
