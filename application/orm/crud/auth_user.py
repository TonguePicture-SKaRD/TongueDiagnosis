import hashlib
from sqlalchemy.orm import Session
from ...models import models


def register_user(email: str, password: str, db: Session):
    """
    当用户注册账号时，将会调用此函数。
    @param email: str, 用户邮箱号
    @param password: str, 用户密码
    @param db: Session, router传入的db，用于链接数据库
    @return: 0 成功注册
             101 用户名/邮箱已经被注册
             102 其他错误
    """
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()  # SHA256加密
    user = models.User(
        email=email,
        password=password
    )  # 创建用户
    if db.query(models.User).filter(models.User.email == email).first():
        # 检查用户名是否存在
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
    """
    当用户登录账户时，将调用此函数。
    @param email: str, 用户邮箱号
    @param password: str, 用户密码
    @param db: Session, router传入的db，用于链接数据库
    @return: 0 成功登录
             101 密码不匹配
             102 其他错误
    """
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()  # SHA256加密
    user = db.query(models.User).filter(models.User.email == email).first()  # 检查用户是否存在
    if user:
        if user.password == password:
            return 0
        else:
            return 102  # 密码不匹配
    else:
        return 101  # 其他错误


def get_user(email: str, db: Session):
    """
    获取用户信息
    @param email: str, 用户邮箱号
    @param db: Session, router传入的db，用于链接数据库
    @return: User.sql, 用户信息
    """
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(email: str, password: str, db: Session):
    """
    验证用户信息
    @param email: str, 用户邮箱号
    @param password: str, 用户密码
    @param db: Session, router传入的db，用于链接数据库
    @return: User.sql, 鉴权后确定可以返回的用户信息
             False, 鉴权后不可返回用户信息
    """
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = get_user(email=email, db=db)
    print(user)
    if not user:
        return False
    if not user.user_password == password:
        return False
    return user


def get_user_record(ID: int, db: Session):
    """
    获取用户的记录
    @param ID: int, 用户ID
    @param db: Session, router传入的db，用于链接数据库
    @return: list[TongueAnalysis.sql], 用户的记录
    """
    return db.query(models.TongueAnalysis).filter(models.TongueAnalysis.user_id == ID).all()
