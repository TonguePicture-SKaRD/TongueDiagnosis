import torch
import torch.nn as nn
import torchvision.transforms.functional as TF


class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DoubleConv, self).__init__()
        self.Conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.Conv(x)


class UNet(nn.Module):
    def __init__(self, down: list = [(3, 64), (64, 128), (128, 256), (256, 512), (512, 1024)],
                 up: list = [(1024, 512), (512, 256), (256, 128), (128, 64)]):
        super().__init__()
        self.up = nn.ModuleList()
        self.down = nn.ModuleList()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        for in_channels, out_channels in down:
            self.down.append(DoubleConv(in_channels, out_channels))

        for in_channels, out_channels in up:
            self.up.append(nn.ConvTranspose2d(in_channels, out_channels, kernel_size=2, stride=2))
            self.up.append(DoubleConv(in_channels, out_channels))

        self.final_conv = nn.Conv2d(64, 1, kernel_size=1)  # 1*1卷积

    def forward(self, x: torch.Tensor):
        skip_connections = []

        for down in self.down:
            x = down(x)
            skip_connections.append(x)
            x = self.pool(x)

        skip_connections.pop()
        skip_connections = skip_connections[::-1]

        for index, up in enumerate(self.up):
            if index % 2 == 1:
                if x.shape != skip_connections[index // 2].shape:
                    x = TF.resize(x, size=skip_connections[index // 2].shape[2:], antialias=True)
                x = torch.cat((skip_connections[index // 2], x), dim=1)
            x = up(x)

        x = self.final_conv(x)
        return x
