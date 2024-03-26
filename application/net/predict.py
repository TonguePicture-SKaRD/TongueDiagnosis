import queue
import tempfile
import torch
import torchvision
from PIL import Image
import numpy as np

from yolov5 import load
from segment_anything import sam_model_registry,SamPredictor


from application.net.model.unet import UNet
from application.net.model.resnet import ResNetPredictor


class TonguePredictor:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,
                 yolo_path='application/net/weights/yolov5.pt',
                 sam_path='application/net/weights/sam_vit_b_01ec64.pth',
                 resnet_path=[
                     'application/net/weights/tongue_color.pth',
                     'application/net/weights/tongue_coat_color.pth',
                     'application/net/weights/thickness.pth',
                     'application/net/weights/rot_and_greasy.pth'
                 ]
                 ):
        if self._initialized:
            return
        self.device = torch.device('cpu')

        # yolov5模型
        self.yolo = load(yolo_path, device='cpu')

        # sam模型
        self.sam = sam_model_registry["vit_b"](checkpoint=sam_path)

        # 残差网络
        self.resnet = ResNetPredictor(resnet_path)
        self.queue = queue.Queue()

        TonguePredictor._initialized = True

    def __predict(self, img, record_id, fun):
        """
        预测舌像
        :param img: 图片文件
        :param record_id: 记录id
        :param fun: 函数
        :return:
        """
        predict_img = Image.open(img)
        # 舌体定位
        self.yolo.eval()
        print("舌体定位")
        with torch.no_grad():
            pred = self.yolo(predict_img)
        if len(pred.xyxy[0]) < 1:
            # 图片不合法
            fun(event_id=record_id,
                tongue_color=None,
                coating_color=None,
                tongue_thickness=None,
                rot_greasy=None,
                code=201)
            print("图片不合法，没舌头")
            return
        elif len(pred.xyxy[0]) > 1:
            # 图片不合法
            fun(event_id=record_id,
                tongue_color=None,
                coating_color=None,
                tongue_thickness=None,
                rot_greasy=None,
                code=202)
            print("图片不合法，舌头太多了")
            return
        # 舌体分割
        print("舌体分割")
        with torch.no_grad():
            x1, y1, x2, y2 = (
                pred.xyxy[0][0, 0].item(), pred.xyxy[0][0, 1].item(), pred.xyxy[0][0, 2].item(),
                pred.xyxy[0][0, 3].item())

            # 切出舌体
            predictor = SamPredictor(sam_model=self.sam)
            predictor.set_image(np.array(predict_img))
            masks, _, _ = predictor.predict(box=np.array([x1, y1, x2, y2]))
            original_img = np.array(predict_img)
            masks = np.transpose(masks, (1,2,0))
            pred = original_img * masks

            result = Image.fromarray(pred).crop((x1, y1, x2, y2)).convert("RGB")
            result = np.array(result)

        result = self.resnet.predict(result)
        print("舌体分析")

        predict_result = {
            "code": 0,
            'tongue_color': result[0],
            'tongue_coat_color': result[1],
            'thickness': result[2],
            'rot_and_greasy': result[3]
        }
        # 保存结果
        fun(event_id=record_id,
            tongue_color=result[0],
            coating_color=result[1],
            tongue_thickness=result[2],
            rot_greasy=result[3],
            code=1)

        return predict_result

    def predict(self, img, record_id, fun):
        """
        复制图片到临时文件，然后放入队列
        :param img:
        :param record_id:
        :param fun:
        :return:
        """
        try:
            img.seek(0)
            tmpfile = tempfile.SpooledTemporaryFile()
            content = img.read()
            tmpfile.write(content)
            self.queue.put((tmpfile, record_id, fun))
            img.seek(0)
            return {"code": 0}
        except Exception as e:
            return {"code": 3}

    def main(self):
        """
        不断读取队列中的图片进行预测
        :return:
        """
        while True:
            if self.queue.empty():
                continue
            img, record_id, fun = self.queue.get()
            try:
                self.__predict(img, record_id, fun)
            except Exception as e:
                print(e)
                fun(event_id=record_id,
                    tongue_color=None,
                    coating_color=None,
                    tongue_thickness=None,
                    rot_greasy=None,
                    code=203)
            finally:
                img.close()


