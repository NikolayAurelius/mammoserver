import numpy as np
from scipy.optimize import minimize_scalar


def grad(weights: np.array, t: float, v: float):
    # TODO: use Cython
    a = weights[0]
    e = weights[1]
    b = weights[2]

    w = weights[3]

    undersin = e + t * w

    sin_value = np.sin(w * t + e)
    cos_value = np.cos(w * t + e)

    dlda = (a * sin_value + b - v) * sin_value
    dlde = a * (a * sin_value + b - v) * cos_value
    dldb = a * sin_value + b - v

    dldw = a * t * (a * sin_value + b - v) * cos_value

    return np.array([dlda, dlde, dldb, dldw])


class Amplitude:
    def __init__(self, raw_measurement: np.array = np.zeros((18, 18, 18, 18, 80))):
        self.raw_measurement = raw_measurement


def raw_measurement_to_amplitude(raw_measurement: np.array = np.zeros((18, 18, 18, 18, 80))):
    # Приравнивать туда-обратно?
    weights = np.random.uniform()

    pass



def real_func(t):
    return 5.0 * np.sin(10.0 * t + 0.5) + 0.1


def loss(a, w, t, e, b, v):
    return (a * np.sin(w * t + e) + b - v) ** 2

dataset = [(t, real_func(t)) for t in range(80)]

samples = 2

w = 10.0
x0 = np.random.uniform(0.1, 3.0, 3)
x0[2] = 0.1
print(x0)
for i in range(1000):
    g = np.zeros((3, ))
    for j in range(samples):
        g += grad(x0[0], w, dataset[j][0], x0[1], x0[2], dataset[j][1])

    g[2] = 0.0
    dx = g / np.linalg.norm(g)

    last_loss = 1e6
    for step in range(100000):
        my_dx = (step / 10000) * dx
        my_x = x0 - my_dx

        my_loss = 0
        for j in range(samples):
            my_loss += loss(my_x[0], w, dataset[j][0], my_x[1], my_x[2], dataset[j][1])
        if my_loss > last_loss:
            print(my_loss)
            break
        last_loss = my_loss
    x1 = x0 - my_dx

    print(x1)
    x0 = x1
    # break







