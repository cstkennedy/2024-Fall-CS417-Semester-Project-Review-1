#! /usr/bin/env python3

"""
This module is a collection of input helpers for the CPU Temperatures Project.
All code may be used freely in the semester project, iff it is imported using
``import parse_temps`` or ``from parse_temps import {...}`` where ``{...}``
represents one or more functions.
"""

import itertools
import re
from typing import Generator, TextIO

import numpy as np
import pprint as pp


def parse_raw_temps(
    original_temps: TextIO, step_size: int = 30
) -> Generator[tuple[float, list[float]], None, None]:
    """
    Take an input file and time-step size and parse all core temps.

    Args:
        original_temps: an input file

        step_size: time-step in seconds

    Yields:
        A tuple containing the next time step and a List containing _n_ core
        temps as floating point values (where _n_ is the number of CPU cores)
    """

    split_re = re.compile(r"[^0-9]*\s+|[^0-9]*$")

    for step, line in enumerate(original_temps):
        yield (
            (step * step_size),
            [float(entry) for entry in split_re.split(line) if len(entry) > 0],
        )


def parse_raw_temps_as_ndarray(
    original_temps: TextIO, step_size: int = 30
) -> tuple[np.ndarray, np.ndarray]:
    """
    Take an input file and time-step size and parse all core temps.

    Args:
        original_temps: an input file

        step_size: time-step in seconds

    Returns:
        T.B.W

    """

    temps = np.loadtxt(original_temps, dtype=np.float64)
    #  pp.pprint(temps)

    num_readings, _ = temps.shape
    times = np.arange(0, num_readings * step_size, step_size)
    #  pp.pprint(times)

    return times, temps
