r"""

:mod:`script` -- Script
=======================

Samsung Multiple Display Control command line tool.

"""

# mandatory imports
import argparse

# relative imports
from samsung_mdc import MultipleDisplayControl, __version__


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
        'data', metavar='value', default=[], type=int, nargs='*',
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
        '-v', '--version', action='version', version=__version__,
        help='Print samsung_mdc version and exit'
    )
    args = parser.parse_args()

    # init object and send command
    with MultipleDisplayControl(args.host, args.port, args.id) as ctrl:
        print(ctrl, end=' .. ')
        if len(args.args) == 0:
            # get
            value = eval(f'ctrl.get_{args.command}()')
            print(f'{args.command} is {value}')
        else:
            # get
            eval(f'ctrl.set_{args.command}(*args.args)')
            args.args = args.args[0] if len(args.args) == 1 else args.args
            print(f'{args.command} set to {args.args}')


if __name__ == "__main__":
    main()
