#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kern FCB 8K0.1 logger

Logs the weight readings from a Kern FCB 8K0.1 balance via the RS232 port to a
file on disk.
"""
__author__ = "Dennis van Gils"
__authoremail__ = "vangils.dennis@gmail.com"
__url__ = "https://github.com/Dennis-van-Gils/project-Kern-FCB-8K0.1-logger"
__date__ = "25-04-2025"
__version__ = "1.0"
# pylint: disable=missing-function-docstring

import re
from typing import Tuple

import numpy as np
from dvg_devices.BaseDevice import SerialDevice


class Kern_FCB_8K01_Balance(SerialDevice):
    """Provides higher-level general I/O methods for communicating with an Kern
    FCB 8K0.1 balance over the RS232 port.
    """

    def __init__(
        self,
        name="Kern",
        long_name="Kern FCB 8K0.1 balance",
    ):
        super().__init__(name=name, long_name=long_name)

        self.serial_settings["baudrate"] = 19200
        self.set_write_termination(None)

    def _parse_weight_reading(self, reading: str) -> Tuple[float, str]:
        """The balance has different reply formats depending on whether the
        reading is considered stable or unstable by the Kern balance, see
        chapter 10.3 of the manual.
        """

        if reading.strip().lower() == "error":
            # raise ValueError(
            print(
                "WARNING: "
                "The balance reports an error! "
                "The maximum load has probably been exceeded."
            )
            return np.nan, ""

        # Regex pattern for a float with optional units
        pattern = r"\b(\d+(?:\.\d+)?)(?:\s*([a-zA-Z%]+))?\b"
        match = re.search(pattern, reading)
        if match:
            float_part = float(match.group(1))
            unit_part = match.group(2) or ""

            return float_part, unit_part

        return np.nan, ""

    def get_stable_weight(self) -> Tuple[float, str]:
        """Get the stable weighing value from the Kern balance.

        Returns:
            `tuple`:
                weight (`float`):
                    Weight value.

                unit (`string`):
                    Unit of the weight value. Note that the unit gets omitted by
                    the Kern balance whenever the reading has not stabilized
                    yet.
        """
        success, reply = self.query("s")
        if not success:
            return np.nan, ""

        return self._parse_weight_reading(reply)

    def get_weight(self) -> Tuple[float, str]:
        """Get the weighing value (stable or unstable) from the Kern balance.

        Returns:
            `tuple`:
                weight (`float`):
                    Weight value.

                unit (`string`):
                    Unit of the weight value. Note that the unit gets omitted by
                    the Kern balance whenever the reading has not stabilized
                    yet.
        """
        success, reply = self.query("w")
        if not success:
            return np.nan, ""

        return self._parse_weight_reading(reply)

    def tare(self) -> bool:
        """Tare the balance."""
        return self.write("t")


# --------------------------------------------------------------------------
#   main
# --------------------------------------------------------------------------


if __name__ == "__main__":
    import datetime
    import os
    from pathlib import Path
    import time

    if os.name == "nt":
        import msvcrt  # pylint:disable=unused-import

    print(
        "Kern FCB 8K0.1 balance logger.\n"
        f"{__url__}\n\n"
        "NOTE on the Kern balance settings:\n"
        "  1) The baud rate (parameter 'bAUd') must be set to 19200.\n"
        "  2) The data transfer mode (parameter 'PR') must be set to 'rE CR'.\n"
        "  3) Recommended: Set the Auto off mode (parameter 'AF') to Off.\n"
        "  4) Recommended: Set the Background illumination of the display\n"
        "     (parameter 'bL') to Off or 'CH' to preserve battery life.\n"
        "\n"
        "USAGE:\n"
        "  Press 'q' or CONTROL+Q to stop acquisition and exit."
    )

    # Try to auto connect to the Kern balance over the RS232 connection
    kern = Kern_FCB_8K01_Balance()
    kern.auto_connect()

    # Auto-generate filename for the log
    log_subfolder = "logs"
    Path(log_subfolder).mkdir(parents=True, exist_ok=True)
    log_filename = Path(log_subfolder).joinpath(
        f"Kern_data_{datetime.datetime.now().strftime("%y%m%d_%H%M%S")}.txt"
    )
    print(f"Logging to: {log_filename}\n")

    # Create log file and start acquisition
    with open(log_filename, "a", encoding="utf-8") as f:
        f.write("time [sec]\tweight\tunit\n")

        running = True
        t0 = time.perf_counter()
        while running:
            t = time.perf_counter() - t0
            weight, unit = kern.get_weight()

            print(f"{t:8.3f}\t{weight:6.1f}\t{unit}")
            f.write(f"{t:.3f}\t{weight:.1f}\t{unit}\n")

            # Catch keypresses in Windows terminal
            if os.name == "nt":
                if msvcrt.kbhit():
                    ms_key = msvcrt.getch()
                    if ms_key == b"q":
                        running = False
