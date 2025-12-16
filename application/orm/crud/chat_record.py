from sqlalchemy.orm import Session
from ...models import models
from datetime import datetime
import time

def get_chat_record(ID: int, sessionid: int, db: Session):
    """
    通过id搜索聊天记录
    :param ID:
    :param sessionid:
    :param db:
    :return:
    """
    db_chat_session = db.query(models.ChatSession).filter(
        models.ChatSession.id == sessionid,
        models.ChatSession.user_id == ID
    ).first()

    if not db_chat_session:
        return 102  # No chat session found
    # 查询所有聊天记录
    chat_records = db.query(models.ChatRecord).filter(
        models.ChatRecord.session_id == sessionid
    ).order_by(models.ChatRecord.create_at).all()

    if not chat_records:
        return 103  # No chat records found
    # # 将毫秒时间戳转换为 datetime
    # for record in chat_records:
    #     if isinstance(record.create_at, int):  # 确保它是一个整数时间戳
    #     record.create_at = datetime.fromtimestamp(record.create_at)  # 转换为秒级时间戳
    #     else:
    #         record.create_at = None  # 如果不是有效的时间戳，设置为 None 或者默认值
    return chat_records

def get_all_chat_id(ID: int, db: Session):
    """
    通过userid搜索所有聊天id
    :param ID:
    :param db:
    :return:
    """
    return db.query(models.ChatSession).filter(
        models.ChatSession.user_id == ID
    ).order_by(models.ChatSession.id).all()

def get_result(img_src: str, db: Session):
    result = db.query(models.TongueAnalysis).filter(models.TongueAnalysis.img_src == img_src).first()
    db.refresh(result)  # 强制刷新查询结果，确保是最新的
    print(result.state)  # 打印结果的状态
    return result

def create_new_session(db: Session,
                       ID: int,
                       tittle: str
                       ):
    new_message = models.ChatSession(
        tittle=tittle,
        user_id=ID
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def create_new_chat_records(db: Session,
                            session_id: int,
                            content: str,
                            role: int
                       ):
    millis_timestamp = int(time.time() * 1000)
    print(millis_timestamp)
    new_message = models.ChatRecord(
        session_id=session_id,
        content=content,
        create_at=millis_timestamp,
        role=role
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message