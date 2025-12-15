from sqlalchemy.orm import Session
from application.models import models
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
    return db.query(models.TongueAnalysis).filter(models.TongueAnalysis.img_src == img_src).first()
