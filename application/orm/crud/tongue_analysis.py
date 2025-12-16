from sqlalchemy.orm import Session
from application.models import models
from fastapi import Depends
from ..database import get_db_object


def write_result(
        event_id: int,
        tongue_color: int,
        coating_color: int,
        tongue_thickness: int,
        rot_greasy: int,
        code: int,
        db: Session = get_db_object()
):
    """
    写入分析结果
    :param event_id: 事件id
    :param tongue_color: 舌色
    :param coating_color: 舌苔颜色
    :param tongue_thickness: 厚薄
    :param rot_greasy: 腐腻
    :param code: 状态码
    :param db: 数据库会话
    0 未完成
    1 已完成
    201 无舌头存在
    202 多个舌头存在
    203 其他错误
    :return:
    0 成功
    1 失败
    """
    record = db.query(models.TongueAnalysis).filter(models.TongueAnalysis.id == event_id).first()
    if code == 1:
        if record:
            record.tongue_color = tongue_color
            record.coating_color = coating_color
            record.tongue_thickness = tongue_thickness
            record.rot_greasy = rot_greasy
            record.state = code
            try:
                db.commit()
                return 0
            except Exception as error:
                db.rollback()
                print(error)
                return 1
    else:
        record.state = code
        try:
            db.commit()
            return 0
        except Exception as error:
            db.rollback()
            print(error)
            return 1


def write_event(
    user_id: int,
    img_src: str,
    state: int,
    db: Session
):
    """
    写入事件
    :param user_id: 用户id
    :param img_src: 图片路径
    :param db: 数据库会话
    :param state: 状态码
    :return:
    """
    event = models.TongueAnalysis(
        user_id=user_id,
        img_src=img_src,
        state=state,
    )
    db.add(event)
    try:
        db.commit()
        return 0
    except Exception as error:
        db.rollback()
        print(error)
        return 201


def get_record_by_location(
    img_src: str,
    db: Session
):
    """
    通过图片路径获取记录
    :param img_src: 图片路径
    :param db: 数据库会话
    :return: models.TongueAnalysis
    """
    return db.query(models.TongueAnalysis).filter(models.TongueAnalysis.img_src == img_src).first()
