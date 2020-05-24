#!/usr/bin/env python3

"""
Automatically removes window urgency hints after a given timeout by
listening for the 'urgent' window event through i3's IPC interface.

Example:
  A messenger application on another workspace receives a new message.
  Normally, it (and thus the workspace) would now be marked as urgent
  in the status bar until the window is focused. While this script is
  running, the urgency hint will be unset after the specified timeout,
  regardless of whether the window was actually focused.

Required Python packages:
  * i3ipc (https://pypi.org/project/i3ipc/)
Required applications:
  * wmctrl (http://tripie.sweb.cz/utils/wmctrl/)

Author: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
License: MIT
"""

import argparse
import logging
import subprocess
import time

import i3ipc


def _parse_args() -> argparse.Namespace:
    """
    Parse and return any provided command line arguments.

    :return: A namespace holding the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Automatically removes window urgency '
                    'hints after a given timeout.')

    parser.add_argument('-s', '--seconds',
                        type=int, metavar='N', default=10,
                        help='urgency hint timeout in seconds '
                             '(default: %(default)d)')

    args: argparse.Namespace = parser.parse_args()

    if args.seconds < 0:
        parser.error('Urgency timeout must be a positive number.')

    return args


def _on_window_urgent(_conn: i3ipc.Connection,
                      event: i3ipc.WindowEvent) -> None:
    """
    Remove a window's urgency hint after the specified timeout.

    :param _conn: A connection to i3's IPC socket
    :param event: The 'urgent' window event
    :return: None
    """
    if not event.container.urgent:
        return

    window_class: str = event.container.window_class
    window_id: int = event.container.window

    logging.info('Detected urgent window "%s" (id: %d)...',
                 window_class, window_id)

    time.sleep(urgency_timeout)
    subprocess.run(['wmctrl', '-r', str(window_id),
                    '-b', 'remove,demands_attention'])

    logging.info('Removed urgency hint from "%s" (id: %d).',
                 window_class, window_id)


def _main() -> None:
    """
    Connect to i3's IPC socket and bind to the 'urgent' window event.

    :return: None
    """
    logging.info('Urgency timeout set to %d seconds. '
                 'Waiting for windows...', urgency_timeout)

    i3conn = i3ipc.Connection()
    i3conn.on(i3ipc.Event.WINDOW_URGENT, _on_window_urgent)
    i3conn.main()


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    urgency_timeout: int = _parse_args().seconds
    _main()
