r"""

:mod:`script` -- Script
=======================

Samsung Multiple Display Control command line tool.

"""

# mandatory imports
import argparse

# relative imports
from .mdc import MultipleDisplayControl
try:
    from .version import version
except (ValueError, ModuleNotFoundError, SyntaxError):
    version = "VERSION-NOT-FOUND"

def main():
    """A simple command-line-tool for direct control of the Samsung Multiple
    Display Control Protocol via TCP/IP
    """

    parser = argparse.ArgumentParser(
        prog='samsung_mdc',
        description='Samsung Multiple Display Control Protocol via TCP/IP',
    )
    parser.add_argument(
        'host', metavar='host', type=str,
        help='Remote TV ipv4-address'
    )

    commands = ('power', 'volume', 'mute', 'source', 'screen_size',
                'video_wall_mode', 'safety_lock', 'video_wall_on',
                'video_wall_user')
    parser.add_argument(
        'command', metavar='command', choices=commands,
        help=('Control command name. Allowed values are: '+', '.join(commands))
    )
    parser.add_argument(
        'data', metavar='value', default=[], nargs='*',
        help=('Data argument(s) for the `set control command` (controlling). '
              'If empty (default), the `get control command` answer '
              '(viewing control state) is printed to stdout.')
    )
    parser.add_argument(
        '-p', '--port', metavar='..', type=int, default=1515,
        help='Remote TV port (default: 1515)'
    )
    parser.add_argument(
        '-i', '--id', metavar='..', type=int, default=254,
        help='Remote TV id (default: 0xfe)'
    )
    parser.add_argument(
        '-t', '--timeout', metavar='..', type=float, default=5.,
        help=('Set a timeout on blocking socket operations, in seconds '
              '(default: 5.0). '
              'Timeout > 0: raise timeout exception. '
              'Timeout == 0: non-blocking mode. '
              'Timeout < 0: blocking mode.')
    )
    parser.add_argument(
        '-v', '--version', action='version', version=version,
        help='Print samsung_mdc version and exit'
    )
    args = parser.parse_args()
    args.timeout = None if args.timeout < 0. else args.timeout  # non-negative

    # init object and send command
    with MultipleDisplayControl(args.host, args.port, args.id,
                                timeout=args.timeout) as ctrl:
        print(ctrl, end=' .. ')
        if len(args.data) == 0:
            # get
            value = eval(f'ctrl.get_{args.command}()')
            print(f'{args.command} is {value}')
        else:
            # get
            args.data = [int(d) if d.isdigit() else d for d in args.data]
            eval(f'ctrl.set_{args.command}(*args.data)')
            args.data = args.data[0] if len(args.data) == 1 else args.data
            print(f'{args.command} set to {args.data}')


if __name__ == "__main__":
    main()
