# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import adafruit_board_toolkit.circuitpython_serial

comports = adafruit_board_toolkit.circuitpython_serial.repl_comports()
if not comports:
    raise Exception("No CircuitPython boards found")

# Print the device paths or names that connect to a REPL.
print([comport.device for comport in comports])
