# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_board_toolkit`
================================================================================

CircuitPython board identification and information


* Author(s): Dan Halbert for Adafruit Industries
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_Board_Toolkit.git"

from typing import Sequence

import os
import sys

import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo

# Some CircuitPython boards do not have interface names that start with "CircuitPython".
INTERFACE_PREFIXES = ("CircuitPython", "Sol", "StringCarM0Ex")


def comports() -> Sequence[ListPortInfo]:
    """Return all the comports recognized as being associated with a CircuitPython board."""

    if sys.platform == "darwin":
        # pyserial 3.5 and below have a bug on MacOS that returns an identical
        # interface name for a composite USB device with multiple device names.
        # For instance, a CircuitPython board with two CDC interfaces
        # "CircuitPython CDC control" and "CircuitPython CDC2 control",
        # presenting as two /dev/cu.* devices, will only show one of those interface names.
        # See https://github.com/pyserial/pyserial/pull/566.
        from . import _list_ports_osx  # pylint: disable=import-outside-toplevel

        ports = _list_ports_osx.comports()
    elif os.name == "nt":
        # pyserial.tools.list_ports_windows does not currently return the interface.
        # This enhanced version does.
        from . import _list_ports_windows  # pylint: disable=import-outside-toplevel

        ports = _list_ports_windows.comports()

    else:
        ports = serial.tools.list_ports.comports()

    return tuple(
        port
        for port in ports
        if port.interface
        and port.interface.startswith(
            tuple((prefix + " CDC" for prefix in INTERFACE_PREFIXES))
        )
    )


def repl_comports() -> Sequence[ListPortInfo]:
    """Return all comports presenting a CircuitPython REPL."""
    # The trailing space in " CDC " is deliberate.
    return tuple(
        port
        for port in comports()
        if port.interface.startswith(
            tuple(prefix + " CDC " for prefix in INTERFACE_PREFIXES)
        )
    )


def data_comports() -> Sequence[ListPortInfo]:
    """Return all comports presenting a CircuitPython serial connection
    used for data transfer, not the REPL.
    """
    # The trailing space in " CDC2 " is deliberate.
    return tuple(
        port
        for port in comports()
        if port.interface.startswith(
            tuple(prefix + " CDC2 " for prefix in INTERFACE_PREFIXES)
        )
    )
