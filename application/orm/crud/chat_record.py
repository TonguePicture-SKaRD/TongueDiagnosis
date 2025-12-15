from sqlalchemy.orm import Session
from ...models import models
import time

def get_chat_record(ID: int, sessionid: int, db: Session):
    db_chat_session = db.query(models.ChatSession).filter(
        models.ChatSession.id == sessionid,
        models.ChatSession.user_id == ID
    ).first()

    if not db_chat_session:
        return 102
    chat_records = db.query(models.ChatRecord).filter(
        models.ChatRecord.session_id == sessionid
    ).order_by(models.ChatRecord.create_at).all()

    if not chat_records:
        return 103
    return chat_records

def get_all_chat_id(ID: int, db: Session):
    return db.query(models.ChatSession).filter(
        models.ChatSession.user_id == ID
    ).order_by(models.ChatSession.id).all()

def get_result(img_src: str, db: Session):
    result = db.query(models.TongueAnalysis).filter(models.TongueAnalysis.img_src == img_src).first()
    db.refresh(result)
    print(result.state)
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