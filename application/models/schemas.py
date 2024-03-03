from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union, Annotated
from fastapi.param_functions import Form


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
        user: UserBase
    }
    """
    data: Union[UserBase, None]


class TongueAnalysisPic(BaseModel):
    """
    fileData: file
    """
    pass


class TongueAnalysisResponse(BaseResponse):
    """
    code: int
    message: str
    data: {
        object: Unknown
    }
    """
    pass


class ExtendedOAuth2PasswordRequestForm:
    def __init__(
            self,
            *,
            email: Annotated[str, Form()],
            password: Annotated[str, Form()],
    ):
        self.email = email
        self.password = password
