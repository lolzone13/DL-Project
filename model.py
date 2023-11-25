import torch
import torch.nn as nn


class QModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.convlayer1 = nn.Sequential(
            nn.Conv2d(3, 96, kernel_size=11, stride=4, padding=0),
            nn.BatchNorm2d(96),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 3, stride = 2))
        self.convlayer2 = nn.Sequential(
            nn.Conv2d(96, 128, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 3, stride = 2))
        
        self.nnImg = nn.Linear(38*38*128, 2048)

        self.nnlayer1 = nn.Linear(289, 512)
        self.nnlayer2 = nn.Linear(512, 512)

        self.fc1 = nn.Linear(2560, 1024)
        self.fc2 = nn.Linear(1024, 9)

        
    def forward(self, img, detect_matrix):
        img = self.convlayer1(img)
        img = self.convlayer2(img)
        img_flat = img.reshape(img.shape[0], -1)
        img_flat = self.nnImg(img_flat)

        x = self.nnlayer1(detect_matrix)
        x = self.nnlayer2(x)

        out = torch.concatenate([x, img_flat], dim=1)
        out = self.fc1(out)
        out = self.fc2(out)
        return out

class Qtrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.model = model
        self.gamma = gamma
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        
    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype = torch.float)
        next_state = torch.tensor(next_state, dtype = torch.float)
        action = torch.tensor(action, dtype = torch.float)
        reward = torch.tensor(reward, dtype = torch.float)
        
        if len(state.shape) == 1:
            #print(state.shape)
            #print(state.unsqueeze(0).shape)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )
            
        pred = self.model(state)
        target = pred.clone()
        for idx in range (len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        
        self.optimizer.step()
        



if __name__ == "__main__":
    sample = torch.rand(1,3,640,640)
    sample2 = torch.rand(1, 289)
    model = QModel()
    output = model(sample, sample2)
    print(output.shape)