from sqlalchemy.orm import Session
from application.models import models


async def analysis_tongue(file_data: str, db: Session):
    """
    分析舌像
    :param file_data: str, 上传舌像图片的文件数据
    :param db: Session, router传入的db，用于链接数据库
    :return: 0 成功分析
             ...
    """
    pass
