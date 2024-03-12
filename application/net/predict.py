import torch
import torchvision
from PIL import Image
import numpy as np

from application.net.model.unet import UNet
from application.net.model.resnet import ResNetPredictor

class TonguePredictor:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,
                 yolo_path = 'application/net/weights/yolov5.pt',
                 unet_path = 'application/net/weights/unet.pth',
                 resnet_path = [
                        'application/net/weights/tongue_color.pth',
                        'application/net/weights/tongue_coat_color.pth',
                        'application/net/weights/thickness.pth',
                        'application/net/weights/rot_and_greasy.pth'
                 ],
                 ):
        self.device = torch.device('cpu')

        # yolov5模型
        self.yolo = torch.hub.load('application/net/yolov5', 'custom', path=yolo_path, source='local').to(self.device)

        # unet模型
        self.unet = UNet()
        self.unet.load_state_dict(torch.load(unet_path,map_location=self.device))

        # 残差网络
        self.resnet = ResNetPredictor(resnet_path)

    def predict(self, img):
        predict_img = Image.open(img)

        # 舌体定位
        self.yolo.eval()
        with torch.no_grad():
            pred = self.yolo(predict_img)
        if len(pred.xyxy) == 0:
            return {"code":1}
        elif len(pred.xyxy) > 1:
            return {"code":2}

        # 舌体分割
        self.unet.eval()
        with torch.no_grad():
            x1, y1, x2, y2 = (pred.xyxy[0][0,0].item(), pred.xyxy[0][0,1].item(), pred.xyxy[0][0,2].item(), pred.xyxy[0][0,3].item())
            split_mask = predict_img.crop((x1, y1, x2, y2))
            split_mask = torchvision.transforms.ToTensor()(split_mask)
            split_mask = split_mask.unsqueeze(0)
            split_mask = split_mask.to(self.device)
            pred = torch.sigmoid(self.unet(split_mask))
            pred = (pred > 0.5)
            pred = np.transpose(pred.cpu().numpy(), (0, 2, 3, 1))
            split_img = predict_img.crop((x1, y1, x2, y2))
            split_img = np.array(split_img)
            result = pred * split_img

        result = np.transpose(result, (0, 3, 1, 2))
        result = self.resnet.predict(result)

        predict_result = {
            "code": 0,
            'tongue_color': result[0],
            'tongue_coat_color': result[1],
            'thickness': result[2],
            'rot_and_greasy': result[3]
        }

        return predict_result


if __name__ == '__main__':
    predictor = TonguePredictor()
    predictor.predict(r'E:\Projects\deeplearning\train_example\data\old\WIN_20240305_18_54_18_Pro.jpg')
