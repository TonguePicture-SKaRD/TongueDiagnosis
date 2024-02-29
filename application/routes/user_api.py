from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from ..core import create_access_token, get_current_user
from ..models import schemas
from ..orm import register_user, login_user, get_user
from ..orm.database import get_db

router_user = APIRouter()


@router_user.post('/register', response_model=schemas.RegisterResponse)
async def register(schema: schemas.UserRegister, db: Session = Depends(get_db)):
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


@router_user.post('/token', response_model=schemas.LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(get_db)):
    """
    登录账号的路由
    @param form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
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
    code = await login_user(email=email, password=password, db=db)
    if code == 0:
        form_data = OAuth2PasswordRequestForm(
            email=email,
            password=password
        )
        token = await create_access_token(data={"email": form_data.email})
        access_token = token
        response = schemas.LoginResponse(
            code=code,
            message='operation success',
            data=schemas.Token(token=access_token)
        )
    elif code == 101:
        response = schemas.LoginResponse(
            code=code,
            message='wrong password'
        )
    else:
        response = schemas.LoginResponse(
            code=code,
            message='operation failed'
        )
    return response


@router_user.get('/info', response_model=schemas.InfoResponse)
async def info_get(user: schemas.User = Depends(get_current_user)):
    """
    获取用户信息的路由
    @param user: User
        email: str
        username: str
    @return: InfoResponse
        code: int
        message: str
        data: User
    """
    if not user:
        return schemas.InfoResponse(
            code=101,
            message="operation failed",
            data=None
        )
    user_data_temp = schemas.UserInfo(
        email=user.email,
    )
    return schemas.InfoResponse(
        code=0,
        message="operation success",
        data=user_data_temp
    )
