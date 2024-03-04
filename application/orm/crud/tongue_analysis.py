from sqlalchemy.orm import Session
from application.models import schemas
from application.models import models


def result_record(
        user_ID: int,
        img_src: str,
        result: schemas.Result,
        db: Session
):
    """
    记录用户分析结果
    :param user_ID: 用户id
    :param img_src: 上传图片路径
    :param result: 分析的结果
    :param db: Session, router传入的db，用于链接数据库
    :return: 0 成功
             202 其他错误
    """
    db_record = models.TongueAnalysis(
        user_id=user_ID,
        img_src=img_src,
        tongue_color=result.tongue_color,
        coating_color=result.coating_color,
        tongue_thickness=result.tongue_thickness,
        rot_greasy=result.rot_greasy
    )

    db.add(db_record)
    try:
        db.commit()
        return 0
    except Exception as error:
        db.rollback()
        print(error)
        return 202
