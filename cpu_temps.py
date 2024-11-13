#! /usr/bin/env python3

import os
import pprint as pp
import sys
from dataclasses import dataclass
from typing import Iterable, Self

import numpy as np

import interpolation
from parse_temps import parse_raw_temps_as_ndarray

# Note: the type keyword requires Python 3.12 or newer
LineDataTuple = tuple[list[int], list[int], list[float], list[float]]


def write_core_file(
    base_name: str,
    core_idx: int,
    line_data: LineDataTuple,
) -> None:
    """
    Output the computed "line" data for a single core where each output line
    takes the form...

       0 <= x <=       30 ; y =      61.0000 +       0.6333 x ; interpolation

    or

       0 <= x <=     3520 ; y =      61.0000 +       0.0003 x ; least-squares
    """

    core_filename = f"{base_name}-core-{core_idx}.txt"

    with open(core_filename, "w") as core_file:
        # TODO: Interpolation output
        for time, time_next, y_int, slope in zip(*line_data):
            core_file.write(
                f"{time:>6} <= x <= {time_next:>6} ;"
                f"y = {y_int:>8.4f} + {slope:>8.4f} x ; interpolation\n"
            )


def main():
    """
    This main function serves as the driver for the demo. Such functions
    are not required in Python. However, we want to prevent unnecessary module
    level (i.e., global) variables.
    """

    # ---------------------------------------------------------------------------
    # Handle CLI
    # ---------------------------------------------------------------------------
    # TODO: Add command line argument validation
    temperature_filename = sys.argv[1]

    # ---------------------------------------------------------------------------
    # Handle input and preprocssing
    # ---------------------------------------------------------------------------
    with open(temperature_filename, "r") as temps_file:
        times, raw_core_data = parse_raw_temps_as_ndarray(temps_file)

        _, num_cores = raw_core_data.shape
        core_data = np.hsplit(raw_core_data, num_cores)
        core_data = [core.flatten() for core in core_data]
        core_temps = core_data

        #  pp.pprint(core_data)


    # ---------------------------------------------------------------------------
    # Process each core and output the results
    # ---------------------------------------------------------------------------
    base_filename = os.path.splitext(temperature_filename)[0]
    for core_idx, core_temps in enumerate(core_temps):
        # interpolation
        raw_line_data = interpolation.piecewise_linear(times, core_temps)

        times_lower, times_upper, y_ints, slopes = raw_line_data

        write_core_file(
            base_filename, core_idx, (times_lower, times_upper, y_ints, slopes)
        )
        # TODO: least squares approximation


"""
def reference_main():
    # ---------------------------------------------------------------------------
    # Handle CLI
    # ---------------------------------------------------------------------------
    # TODO: Add command line argument validation
    input_temps = sys.argv[1]

    # ---------------------------------------------------------------------------
    # Handle input and preprocssing
    # ---------------------------------------------------------------------------
    with open(input_temps, "r") as temps_file:

        times, raw_core_data = parse_raw_temps_as_ndarray(temps_file)

        _, num_cores = raw_core_data.shape
        core_data = np.hsplit(raw_core_data, num_cores)
        core_data = [core.flatten() for core in core_data]

    # ---------------------------------------------------------------------------
    # Process each core and output the results
    # ---------------------------------------------------------------------------
    base_filename = os.path.splitext(input_temps)[0]
    for core_idx, core_temps in enumerate(core_data):
        raw_line_data = interpolation.piecewise_linear(times, core_temps)

        # TODO: least squares approximation
        #  slope, y_int = least_squares.linear(times, core_temps)

        write_core_file(base_filename, core_idx, raw_line_data)
"""

if __name__ == "__main__":
    main()
