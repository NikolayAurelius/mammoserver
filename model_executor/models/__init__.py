import torch
import torch.nn as nn
import torch.nn.functional as F
from .common import conv4d
import os
from scipy.stats import tmean, tmin, tmax, tstd
from sklearn.metrics import log_loss

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
WORKDIR = os.path.dirname(os.path.abspath(__file__))


class Model1(nn.Module):
    def __init__(self):
        super(Model1, self).__init__()
        self.name = 'torch_model_1'

        self.head = nn.Sequential(
            conv4d(1, 3, 4),
            nn.ReLU(inplace=True),
            conv4d(3, 9 // 3, 4),
            nn.ReLU(inplace=True),
            conv4d(9 // 3, 12 // 3, 4),
            nn.ReLU(inplace=True),
            conv4d(12 // 3, 15 // 3, 4),
            nn.ReLU(inplace=True),
            conv4d(15 // 3, 15 // 3, 3),
            nn.ReLU(inplace=True)
        )

        self.out = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(15 * ((18 - 14) ** 4) // 3, 100 // 3),
            nn.ReLU(inplace=True),
            nn.Linear(100 // 3, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.out(self.head(x))


class Model2(nn.Module):
    def __init__(self):
        super(Model2, self).__init__()
        self.name = 'torch_model_2'

        self.head = nn.Sequential(
            conv4d(1, 3, 4),
            nn.ReLU(inplace=True),
            conv4d(3, 9, 4),
            nn.ReLU(inplace=True),
            conv4d(9, 12, 4),
            nn.ReLU(inplace=True),
            conv4d(12, 15, 4),
            nn.ReLU(inplace=True),
            conv4d(15, 15, 3),
            nn.ReLU(inplace=True),


        )

        self.out = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(15 * ((18 - 14) ** 4), 100),
            nn.ReLU(inplace=True),
            nn.Linear(100, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.out(self.head(x))


class ModelSimple(nn.Module):
    def __init__(self):
        super(ModelSimple, self).__init__()
        self.name = 'torch_model_3'

        self.head = nn.Sequential(
            conv4d(1, 5, 7),
            nn.ReLU(inplace=True),
            conv4d(5, 10, 7),
            nn.ReLU(inplace=True),
        )

        self.out = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(10 * ((18 - 12) ** 4), 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.out(self.head(x))


class ModelSimplest(nn.Module):
    def __init__(self):
        super(ModelSimplest, self).__init__()
        self.name = 'torch_model_4'

        self.head = nn.Sequential(
            conv4d(1, 3, 13),
            nn.ReLU(inplace=True)
        )

        self.out = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(3 * (18 - 12) ** 4, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.out(self.head(x))


model_1 = Model1().to(device=device)
model_1.load_state_dict(torch.load(f'{WORKDIR}/torch_model_1.pt', map_location=torch.device('cpu')))
model_1.eval()

model_2 = Model2().to(device=device)
model_2.load_state_dict(torch.load(f'{WORKDIR}/torch_model_2.pt', map_location=torch.device('cpu')))
model_2.eval()

model_3 = ModelSimple().to(device=device)
model_3.load_state_dict(torch.load(f'{WORKDIR}/torch_model_3.pt', map_location=torch.device('cpu')))
model_3.eval()

model_4 = ModelSimplest().to(device=device)
model_4.load_state_dict(torch.load(f'{WORKDIR}/torch_model_4.pt', map_location=torch.device('cpu')))
model_4.eval()


def g(value):
    if value > 1.0:
        value = 1.0
    elif value < -1.0:
        value = -1.0
    value = int((value + 1.0) * 50)
    return value


def bad(x):
    plane_orig = x.view(-1)
    bad_vector = [tmean(plane_orig, limits=(0.0, 10 ** 6), inclusive=(False, True)),
                  tmin(plane_orig, lowerlimit=0.0, inclusive=False),
                  tmax(plane_orig),
                  tstd(plane_orig, limits=(0.0, 10 ** 6), inclusive=(False, True))]
    bad_weights = [0.00169841, 0.01075043, -0.00035599, 0.00358488]
    bad = -2.49578006
    for i in range(len(bad_vector)):
        bad += bad_weights[i] * bad_vector[i]
    bad = g(bad)
    return bad


def stranger(y_pred):
    known_vector = [log_loss([[1.0, 0.0]], y_pred), log_loss([[0.0, 1.0]], y_pred)]
    known_weights = [-0.05717982, -0.06803618]
    known = 0.6073612
    for i in range(len(known_vector)):
        known += known_weights[i] * known_vector[i]
    known = g(known)
    return known


def cancer(x):
    return int(model_2(x)[0].item() * 1000)
