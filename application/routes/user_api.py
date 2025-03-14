"""
与用户相关的路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from ..core import create_access_token, get_current_user
from ..models import schemas
from ..orm import register_user, login_user, get_user, get_user_record
from ..orm.database import get_db

router_user = APIRouter()


@router_user.post('/register', response_model=schemas.RegisterResponse)
def register(schema: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    注册账户的路由
    @param schema: UserRegister
        email: str
        password: str
    @param db: 路由传回的当前会话的db，获取数据库链接
    @return: RegisterResponse
            code: int
            message: str
            data: None
    """
    password = schema.password
    email = schema.email
    code = register_user(email=email, password=password, db=db)
    if code == 0:
        response = schemas.RegisterResponse(code=code, message='operation success')
    elif code == 101:
        response = schemas.RegisterResponse(code=code, message='has been registered')
    else:
        response = schemas.RegisterResponse(code=code, message='operation failed')
    return response


@router_user.put('/login', response_model=schemas.LoginResponse)
def login(form_data: Annotated[schemas.ExtendedOAuth2PasswordRequestForm, Depends()],
          db: Session = Depends(get_db)):
    """
    登录账号的路由
    @param form_data: Annotated[schemas.ExtendedOAuth2PasswordRequestForm, Depends()]
        ID: str
        email: str
        password: str
    @param db: 路由传回的当前会话的db，获取数据库链接
    @return: LoginResponse
        code: int
        message: str
        data: Token
    """
    email = form_data.email
    password = form_data.password
    code = login_user(email=email, password=password, db=db)
    if code == 0:
        user = get_user(email=email, db=db)
        token = create_access_token(data={"ID": user.id, "email": form_data.email})
        access_token = token
        response = schemas.LoginResponse(
            code=code,
            message='operation success',
            data=schemas.Token(token=access_token)
        )
    elif code == 101:
        response = schemas.LoginResponse(
            code=code,
            message='operation failed',
            data=None
        )
    else:
        response = schemas.LoginResponse(
            code=code,
            message='wrong password',
            data=None
        )
    return response


@router_user.get('/info', response_model=schemas.InfoResponse)
def info_get(user: schemas.UserBase = Depends(get_current_user)):
    """
    获取用户信息的路由
    @param user: User
    @return: InfoResponse
        code: int
        message: str
        data: UserBase
            ID: int
            email: str
    """
    if not user:
        return schemas.InfoResponse(
            code=101,
            message="operation failed",
            data=None
        )
    user_data_temp = schemas.UserBase(
        ID=user.id,
        email=user.email
    )
    return schemas.InfoResponse(
        code=0,
        message="operation success",
        data=user_data_temp
    )


@router_user.get('/record', response_model=schemas.RecordResponse)
def record_get(user: schemas.UserBase = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    获取用户记录的路由
    @param user: User
    @param db: Session, router传入的db，用于链接数据库
    @return: RecordResponse
        code: int
        message: str
        data: List[Record]
            ID: int
            pic: str
            result: Result

    """
    if not user:
        return schemas.RecordResponse(
            code=101,
            message="operation failed",
            data=[]
        )
    else:
        user_record = get_user_record(ID=user.id, db=db)
        data_temp = []
        for record in user_record:
            data_temp.append(schemas.Record(
                ID=record.id,
                user_ID=record.user_id,
                img_src=record.img_src,
                state=record.state,
                result=schemas.Result(
                    tongue_color=record.tongue_color,
                    coating_color=record.coating_color,
                    tongue_thickness=record.tongue_thickness,
                    rot_greasy=record.rot_greasy
                )
            ))
        return schemas.RecordResponse(
            code=0,
            message="operation success",
            data=data_temp
        )
