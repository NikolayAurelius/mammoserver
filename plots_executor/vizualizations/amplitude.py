import numpy as np


# def grad(weights: np.array, t: float, v: float):
#     # TODO: use Cython
#     a = weights[0]
#     e = weights[1]
#     b = weights[2]
#
#     w = weights[3]
#
#     undersin = e + t * w
#
#     sin_value = np.sin(w * t + e)
#     cos_value = np.cos(w * t + e)
#
#     dlda = (a * sin_value + b - v) * sin_value
#     dlde = a * (a * sin_value + b - v) * cos_value
#     dldb = a * sin_value + b - v
#
#     dldw = a * t * (a * sin_value + b - v) * cos_value
#
#     return np.array([dlda, dlde, dldb, dldw])


class Amplitude:
    def __init__(self, raw_measurement: np.array = np.zeros((18, 18, 18, 18, 80))):
        self.raw_measurement = raw_measurement


def max_min_approximate_aplitude(meas):
    meas = np.sort(meas, axis=4)
    return np.abs(meas[:, :, :, :, -1] - meas[:, :, :, :, 0]) / 2


def meas_to_x(meas: np.array = np.zeros((18, 18, 18, 18, 80))):
    amplitude = max_min_approximate_aplitude(meas)
    x = np.expand_dims(np.expand_dims(amplitude, axis=0), axis=0)
    return x

