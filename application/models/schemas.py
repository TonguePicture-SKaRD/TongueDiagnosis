from pydantic import BaseModel
from typing import Union


class BaseResponse(BaseModel):
    """
    code: int
    message: str
    data: Any
    """
    code: int
    message: str
    data: Union[dict, list] = None


class Token(BaseModel):
    """
    token: str
    """
    token: str


class UserBase(BaseModel):
    """
    id int
    email str
    """
    id: int = None
    email: str


class UserAuth(UserBase):
    """
    id int
    email str
    password str
    """
    password: str


class UserLogin(BaseModel):
    """
    email: str
    password: str
    """
    email: str
    password: str


class UserRegister(BaseModel):
    """
    email: str
    password: str
    """
    email: str
    password: str


class UserInfo(UserBase):
    """
    email: str
    """
    email: str


class LoginResponse(BaseResponse):
    """
    code: int
    message: str
    data: {
        token: str
    }
    """
    data: Union[Token, None]


class RegisterResponse(BaseResponse):
    """
    code: int
    message: str
    data: None
    """
    pass


class InfoResponse(BaseResponse):
    """
    code: int
    message: str
    data: {
        user: UserInfo
    }
    """
    data: Union[UserInfo, None]
