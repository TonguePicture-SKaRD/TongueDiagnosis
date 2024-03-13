import torch
import torch.nn as nn
import torchvision.transforms.functional as TF


class DoubleConv(nn.Module):
    """
    双卷积层
    (conv => BN => ReLU) * 2
    """

    def __init__(self, in_channels, out_channels):
        """

        :param in_channels:输入通道数
        :param out_channels: 输出通道数
        """
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
        """
        初始化
        :param down:下采样通道数
        :param up: 上采样通道数
        """
        super().__init__()
        self.up = nn.ModuleList()  # 上采样
        self.down = nn.ModuleList()  # 下采样
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)  # 最大池化

        for in_channels, out_channels in down:  # 下采样
            self.down.append(DoubleConv(in_channels, out_channels))

        for in_channels, out_channels in up:  # 上采样
            self.up.append(nn.ConvTranspose2d(in_channels, out_channels, kernel_size=2, stride=2))
            self.up.append(DoubleConv(in_channels, out_channels))

        self.final_conv = nn.Conv2d(64, 1, kernel_size=1)  # 1*1卷积

    def forward(self, x: torch.Tensor):
        """
        前向传播
        :param x:
        :return:
        """
        skip_connections = []  # 存储下采样的特征图

        for down in self.down:  # 下采样
            x = down(x)
            skip_connections.append(x)
            x = self.pool(x)

        skip_connections.pop()  # 删除最后一层
        skip_connections = skip_connections[::-1]  # 反转

        for index, up in enumerate(self.up):  # 上采样
            if index % 2 == 1:
                if x.shape != skip_connections[index // 2].shape:
                    x = TF.resize(x, size=skip_connections[index // 2].shape[2:], antialias=True)
                x = torch.cat((skip_connections[index // 2], x), dim=1)
            x = up(x)  # 上采样

        x = self.final_conv(x)

        return x
