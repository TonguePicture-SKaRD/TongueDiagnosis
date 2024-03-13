import os
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from tempfile import SpooledTemporaryFile

from ..core import get_current_user
from ..models import schemas
from ..orm.database import get_db
from ..orm import write_event, write_result, get_record_by_location
from ..config import Settings

from ..net import TonguePredictor

router_tongue_analysis = APIRouter()


@router_tongue_analysis.post('/upload', response_model=schemas.UploadResponse)
async def upload(file_data: UploadFile,
                 user: schemas.UserBase = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):
    """
    上传舌头图片的路由
    @param file_data: schemas.Upload
        fileData: UploadFile
    @param user: User，当前用户信息
    @param db: 路由传回的当前会话的db，获取数据库链接
    @return: TongueAnalysisResponse
        code: int  # 0表示图片上传成功，201表示图片上传失败
        message: str
    """

    # 模型分析
    def analysis(img: SpooledTemporaryFile, record_id: int, function):
        """
        模型分析
        :param img: 图片
        :param record_id: 事件id
        :param function: 保存结果的函数
        :return: None
        """
        predictor = TonguePredictor()
        predictor.predict(img=img, record_id=record_id, fun=function)

    # 保存图片
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file_data.filename)[1]
    filename = f"{timestamp}{file_extension}"
    file_location = f"{Settings.IMG_PATH}/{filename}"
    with open(file_location, "wb") as f:
        contents = await file_data.read()
        f.write(contents)

    # 写入事件
    code = write_event(user_id=user.id, img_src=file_location, state=0, db=db)

    # 模型调用
    if code == 0:
        record = get_record_by_location(file_location, db=db)
        analysis(img=file_data.file, record_id=record.id, function=write_result)
        return schemas.UploadResponse(
            code=0,
            message="operation success",
            data=None
        )
    else:
        return schemas.UploadResponse(
            code=201,
            message="operation failed",
            data=None
        )
