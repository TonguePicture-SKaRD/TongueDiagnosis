from sqlalchemy.orm import Session
from ...models import models
from datetime import datetime

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
    # 将毫秒时间戳转换为 datetime
    for record in chat_records:

        if isinstance(record.create_at, int):  # 确保它是一个整数时间戳
            record.create_at = datetime.fromtimestamp(record.create_at / 1000)  # 转换为秒级时间戳
        else:
            record.create_at = None  # 如果不是有效的时间戳，设置为 None 或者默认值

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