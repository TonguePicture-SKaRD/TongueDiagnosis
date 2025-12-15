import hashlib
from sqlalchemy.orm import Session
from ...models import models

def register_user(email: str, password: str, db: Session):
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()  # SHA256加密
    user = models.User(
        email=email,
        password=password
    )
    if db.query(models.User).filter(models.User.email == email).first():
        return 101
    db.add(user)
    try:
        db.commit()
        return 0
    except Exception as error:
        db.rollback()
        print(error)
        return 102


def login_user(email: str, password: str, db: Session):
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()  # SHA256加密
    user = db.query(models.User).filter(models.User.email == email).first()  # 检查用户是否存在
    if user:
        if user.password == password:
            return 0
        else:
            return 102
    else:
        return 101

def get_user(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(email: str, password: str, db: Session):
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = get_user(email=email, db=db)
    print(user)
    if not user:
        return False
    if not user.user_password == password:
        return False
    return user


def get_user_record(ID: int, db: Session):
    return db.query(models.TongueAnalysis).filter(models.TongueAnalysis.user_id == ID).all()
