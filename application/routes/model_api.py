from fastapi import APIRouter, Depends,UploadFile
from sqlalchemy.orm import Session

from ..core import get_current_user
from ..models import schemas
from ..orm.database import get_db
from ..orm.crud import result_record

from ..net.predict import TonguePredictor
import time

router_tongue_analysis = APIRouter()


@router_tongue_analysis.post('/upload')
def upload(fileData: UploadFile,
           user: schemas.UserBase = Depends(get_current_user),
           db: Session = Depends(get_db)
           ):
    """
    上传舌头图片的路由
    @param fileData: TongueAnalysisPic
        fileData: file
    @param user: User，当前用户信息
    @param db: 路由传回的当前会话的db，获取数据库链接
    @return: TongueAnalysisResponse
        code: int
        message: str
        data: object
    """

    # def get_file(file_data):
    #     """
    #     获取文件
    #     等待和前端对接
    #     :param file_data: 文件传入方式
    #     :return: 图片文件
    #     """
    #     print(file_data)
    #     return 1
    #
    # def analysis_tongue_pic(file):
    #     """
    #     调用模型分析舌头图片
    #     等待和模型端对接
    #     :param file: 图片文件
    #     :return: schemas.Result 分析结果
    #     """
    #     print(file)
    #     try:
    #         # 调用模型
    #         result = schemas.Result(
    #             tongue_color=0,
    #             coating_color=2,
    #             tongue_thickness=1,
    #             rot_greasy=0
    #         )
    #     except Exception as error:
    #         print(error)
    #         result = None
    #     return result
    #
    # file_pic = get_file(fileData.fileData)
    # result_temp = analysis_tongue_pic(file_pic)
    # if result_temp:
    #     code = result_record(
    #         user_ID=user.id,
    #         img_src=fileData.fileData,  # 待与前端对接文件格式
    #         result=result_temp,
    #         db=db
    #     )
    #     if code == 0:
    #         return schemas.UploadResponse(
    #             code=code,
    #             message="operation success",
    #             data=result_temp
    #         )
    #     else:
    #         return schemas.UploadResponse(
    #             code=code,
    #             message="operation failed",
    #             data=None
    #         )
    # else:
    #     return schemas.UploadResponse(
    #         code=201,
    #         message="The picture is illegal",
    #         data=None
    #     )


    tongue_predictor = TonguePredictor()
    result = tongue_predictor.predict(fileData.file,1,lambda **kwargs: print(kwargs))

    return result