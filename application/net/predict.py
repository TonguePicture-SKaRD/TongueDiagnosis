import torch
import torchvision
from PIL import Image
import numpy as np

from application.net.model.unet import UNet
from application.net.model.resnet import ResNet50

class TonguePredictor:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,
                 yolo_path = 'application/net/weights/best.pt',
                 unet_path = 'application/net/weights/unet.pth',
                 resnet_path = [],
                 ):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # yolov5模型
        self.yolo = torch.hub.load('./yolov5', 'custom', path=yolo_path, source='local').to(self.device)

        # unet模型
        self.unet = UNet()
        self.unet.load_state_dict(torch.load(unet_path))

        # 残差网络
        self.resnet = ResNet50(5,True).to(self.device)

    def predict(self, img):
        predict_img = Image.open(img)

        # 舌体定位
        self.yolo.eval()
        with torch.no_grad():
            pred = self.yolo(predict_img)
        if pred.xyxy.shape[0] == 0:
            return 1

        # 舌体分割
        self.unet.eval()
        with torch.no_grad():
            x1, y1, x2, y2 = (pred.xyxy[0][0,0], pred.xyxy[0][0,1], pred.xyxy[0][0,2], pred.xyxy[0][0,3])
            split_mask = predict_img.crop((x1, y1, x2, y2))
            split_mask = torchvision.transforms.ToTensor()(split_mask)
            split_mask = split_mask.unsqueeze(0)
            split_mask = split_mask.to(self.device)
            pred = torch.sigmoid(self.unet(split_mask))
            pred = (pred > 0.5)
            pred = np.transpose(pred.cpu().numpy(), (0, 2, 3, 1))
            split_img = predict_img.crop((x1, y1, x2, y2))
            split_img = np.array(split_img)
            result = img * pred
            result = np.squeeze(result, axis=0)
