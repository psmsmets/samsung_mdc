r"""

:mod:`helpers` -- Helpers
======================================

Samsung Multiple Display Control helpers

"""

# mandatory imports
import socket


__all__ = ['is_valid_ipv4_address', 'verify_key_value']


def is_valid_ipv4_address(address):
    """Returns True if a valid ipv4 address is given otherwise False.
    """
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True


def verify_key_value(key_value, keys_values: dict, name: str = None):
    """Verify a key or value with a dictionary.

    Parameters:
    -----------
    key_value: `str` or `int`
        The key (integer) or value (string, case insensitive) to be verified
        with ``keys_values``.

    keys_values: `dict`
        Dictionary with integer/hexadecimal keys and string values.

    name: `str`, optional
        Name of the command or option

    Returns:
    --------

    key: `int`
        Integer key of ``key_value`` in ``keys_values``.

    Raises:
    ------
    TypeError:
        When ``key_value`` is anything but a `str` or `int`.

    ValueError
        When ``key_value`` is not found in ``keys_values``.
    """
    name = name or 'key_value'
    if not isinstance(name, str):
        raise TypeError('name should be of type string')

    def raise_value_error():
        raise ValueError(f'{name} key or value "{key_value}" is invalid. '
                         f'Select any of {keys_values}')

    if not all(isinstance(key, (int)) for key in keys_values.keys()):
        raise TypeError('keys_values keys should all be integers')
    if not all(isinstance(val, (str)) for val in keys_values.values()):
        raise TypeError('keys_values values should all be strings')

    if isinstance(key_value, str):
        for key, val in keys_values.items():
            if key_value.lower() == val.lower():
                break
        else:
            raise_value_error()
        key_value = key
    elif isinstance(key_value, int):
        if key_value not in keys_values:
            raise_value_error()
    else:
        raise TypeError(f'{name} should be a either a string or integer')

    return key_value
