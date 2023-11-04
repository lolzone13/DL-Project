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



if __name__ == "__main__":
    sample = torch.rand(1,3,640,640)
    sample2 = torch.rand(1, 289)
    model = QModel()
    output = model(sample, sample2)
    print(output.shape)