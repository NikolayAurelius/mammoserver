import torch
import torch.nn as nn
import torch.nn.functional as F
from ..common import conv4d
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
WORKDIR = os.path.dirname(os.path.abspath(__file__))


class Model2(nn.Module):
    def __init__(self):
        super(Model2, self).__init__()
        self.name = 'torch_model_2'
        self.conv1 = conv4d(1, 3, 4)
        self.conv2 = conv4d(3, 9, 4)

        self.conv3 = conv4d(9, 12, 4)
        self.conv4 = conv4d(12, 15, 4)

        self.conv5 = conv4d(15, 15, 3)

        self.dense1 = nn.Linear(15 * ((18 - 14) ** 4), 100)
        self.dense2 = nn.Linear(100, 2)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))

        x = nn.Flatten()(x)

        x = nn.Dropout(0.5)(x)

        x = F.relu(self.dense1(x))

        return nn.Softmax(dim=1)(self.dense2(x))


model_2 = Model2().to(device=device)
model_2.load_state_dict(torch.load(f'{WORKDIR}/model1.pt', map_location=torch.device('cpu')))
model_2.eval()


class Model1(nn.Module):
    def __init__(self):
        super(Model1, self).__init__()
        self.name = 'torch_model_1'
        self.conv1 = conv4d(1, 3, 4)
        self.conv2 = conv4d(3, 9 // 3, 4)
        self.conv3 = conv4d(9 // 3, 12 // 3, 4)
        self.conv4 = conv4d(12 // 3, 15 // 3, 4)
        self.conv5 = conv4d(15 // 3, 15 // 3, 3)
        self.dense1 = nn.Linear(15 * ((18 - 14) ** 4) // 3, 100 // 3)
        self.dense2 = nn.Linear(100 // 3, 2)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        x = nn.Flatten()(x)
        x = nn.Dropout(0.5)(x)
        x = F.relu(self.dense1(x))
        return nn.Softmax(dim=1)(self.dense2(x))


model_1 = Model1().to(device=device)
model_1.load_state_dict(torch.load(f'{WORKDIR}/model1div3.pt', map_location=torch.device('cpu')))
model_1.eval()


class ModelSimple(nn.Module):
    def __init__(self):
        super(ModelSimple, self).__init__()
        self.name = 'torch_model_3'
        self.conv1 = conv4d(1, 5, 7)
        self.conv2 = conv4d(5, 10, 7)
        self.dense2 = nn.Linear(10 * ((18 - 12) ** 4), 2)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = nn.Flatten()(x)
        x = nn.Dropout(0.5)(x)
        return nn.Softmax(dim=1)(self.dense2(x))


model_3 = ModelSimple().to(device=device)
model_3.load_state_dict(torch.load(f'{WORKDIR}/model_simple1.pt', map_location=torch.device('cpu')))
model_3.eval()


class ModelSimplest(nn.Module):
    def __init__(self):
        super(ModelSimplest, self).__init__()
        self.name = 'torch_model_4'
        self.conv1 = conv4d(1, 3, 13)
        self.dense1 = nn.Linear(3 * (18 - 12) ** 4, 2)

    def forward(self, x):
        x = nn.Dropout(0.15)(x)
        x = F.relu(self.conv1(x))
        x = nn.Flatten()(x)
        x = nn.Dropout(0.5)(x)
        return nn.Softmax(dim=1)(self.dense1(x))


model_4 = ModelSimplest().to(device=device)
model_4.load_state_dict(torch.load(f'{WORKDIR}/model_simplest1.pt', map_location=torch.device('cpu')))
model_4.eval()
