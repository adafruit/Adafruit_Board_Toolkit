# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import adafruit_board_toolkit

devices = adafruit_board_toolkit.usb_devices
if not devices:
    raise Exception("No CircuitPython boards found")

# Print the device path or name used to connect to the REPL.
print(adafruit_board_toolkit.usb_devices[0].repl_serial_device)
