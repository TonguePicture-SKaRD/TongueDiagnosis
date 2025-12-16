import torch
import torch.nn as nn
from torchvision import transforms


class BottleNeckDeep(nn.Module):
    """深层残差块"""

    def __init__(self, in_channels: int, out_channels: int, stride: int = 1, momentum: int = 0.1,
                 if_downsample: int = False, se_block=None):
        """
        初始化
        :param in_channels: 输入通道数
        :param out_channels: 输出通道的四分之一，因为不想写除法
        :param stride: 步长
        :param momentum: bn的动量
        :param if_downsample: 是否对x进行变换
        """
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=1, stride=1, bias=False)
        self.bn1 = nn.BatchNorm2d(num_features=out_channels, momentum=momentum)
        self.conv2 = nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(num_features=out_channels, momentum=momentum)
        self.conv3 = nn.Conv2d(in_channels=out_channels, out_channels=out_channels * 4, kernel_size=1, stride=1,
                               bias=False)
        self.bn3 = nn.BatchNorm2d(num_features=out_channels * 4, momentum=momentum)

        # 用于处理输入和输出通道数不一致的情况
        if if_downsample:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_channels=in_channels, out_channels=out_channels * 4, kernel_size=1, stride=stride,
                          bias=False),
                nn.BatchNorm2d(num_features=out_channels * 4)
            )
        else:
            self.downsample = None

        if se_block is not None:
            self.seNet = se_block(out_channels * 4)

    def forward(self, x):
        """
        前向传播
        :param x: 输入
        :return:
        """
        y = self.conv1(x)
        y = self.bn1(y)
        y = torch.relu(y)
        y = self.conv2(y)
        y = self.bn2(y)
        y = torch.relu(y)
        y = self.conv3(y)
        y = self.bn3(y)
        if self.seNet is not None:
            y = torch.relu(y)
            y = self.seNet(y)
        if self.downsample:
            x = self.downsample(x)
        y += x
        y = torch.relu(y)
        return y


class ResNetDeep(nn.Module):
    """resnet深层网络"""

    def __init__(self, block_num: list, num_classes=2, se_block=None):
        """
        初始化
        :param block_num: 每个残差块的数量
        :param num_classes: 类别数量
        """
        super().__init__()

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(num_features=64, momentum=0.1)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(in_channels=64, out_channels=64, blocks=block_num[0], stride=1,
                                       se_block=se_block)
        self.layer2 = self._make_layer(in_channels=256, out_channels=128, blocks=block_num[1], stride=2,
                                       se_block=se_block)
        self.layer3 = self._make_layer(in_channels=512, out_channels=256, blocks=block_num[1], stride=2,
                                       se_block=se_block)
        self.layer4 = self._make_layer(in_channels=1024, out_channels=512, blocks=block_num[1], stride=2,
                                       se_block=se_block)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        self.fc = nn.Linear(2048, num_classes)

    def _make_layer(self, in_channels, out_channels, blocks, stride=1, se_block=None):
        """
        创建层
        :param in_channels: 输入通道数
        :param out_channels: 输出通道的四分之一
        :param blocks: 层数
        :param stride: 步长
        :return:
        """
        layers = []
        layers.append(BottleNeckDeep(in_channels, out_channels, stride=stride, if_downsample=True, se_block=se_block))
        for _ in range(1, blocks):
            layers.append(BottleNeckDeep(out_channels * 4, out_channels, se_block=se_block))
        return nn.Sequential(*layers)

    def forward(self, x: torch.tensor):
        """
        前向传播
        :param x:
        :return:
        """
        x = self.conv1(x)
        x = self.bn1(x)
        x = torch.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = x.flatten(1)
        x = self.fc(x)

        return x


class SeNet(nn.Module):
    """挤压网络"""

    def __init__(self, in_channels: int, r: int = 16):
        """
        初始化
        :param in_channels: 输入通道数
        :param r: 是一个超参数表示两个全连接层之间差多少
        """
        super().__init__()
        self.AvagePool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc1 = nn.Linear(in_channels, in_channels // r)
        self.fc2 = nn.Linear(in_channels // r, in_channels)

    def forward(self, x: torch.Tensor):
        """
        前向传播
        :param x: 输入
        :return:
        """
        y = self.AvagePool(x)
        y = y.view(y.size(0), -1)
        y = torch.relu(self.fc1(y))
        y = torch.sigmoid(self.fc2(y))
        y = y.view(y.size(0), y.size(1), 1, 1)
        return x * y


def ResNet50(num_classes=2, if_se=False):
    """
    创建resnet50
    :param if_se:
    :param num_classes: 类别数
    :return:
    """
    if if_se:
        return ResNetDeep(block_num=[3, 4, 6, 3], num_classes=num_classes, se_block=SeNet)
    return ResNetDeep(block_num=[3, 4, 6, 3], num_classes=num_classes)


class ResNetPredictor:
    def __init__(self, path: list, tasks: list = [5, 3, 2, 2]):
        self.device = 'cpu'
        self.nets = []
        self.transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize(mean=[0.29, 0.22, 0.23], std=[0.34, 0.27, 0.28])])
        for p in range(len(path)):
            net = ResNet50(tasks[p], True).to(self.device)
            net.load_state_dict(torch.load(path[p], map_location=self.device))
            net.eval()
            self.nets.append(net)

    def predict(self, img):

        img = self.transform(img)
        img = img.unsqueeze(0).to(self.device)

        result = []
        for net in self.nets:
            with torch.no_grad():
                pred = net(img)
                pred = torch.softmax(pred, dim=1)
                pred = torch.argmax(pred, dim=1).cpu().item()
                result.append(pred)

        return result
