"""
T.B.W.
"""

import numpy as np


def piecewise_linear(times: list[float], temperatures: list[float]):
    """
    T.B.W.

    Yields:
        tuples in the form...

        (start time, end time, y-intercept, slope)
    """

    slopes = (temperatures[1:] - temperatures[0:-1]) / (times[1:] - times[0:-1])
    y_ints = temperatures[1:] - (slopes * times[1:])

    return (times[0:-1], times[1:], y_ints, slopes)



# Notes: np.column_stack((a,b))
