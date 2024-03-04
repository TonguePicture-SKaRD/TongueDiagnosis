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
    ID int
    email str
    """
    ID: int = None
    email: str


class UserAuth(UserBase):
    """
    ID int
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


class Result(BaseModel):
    """
    tongue_color: int
    coating_color: int
    tongue_thickness: int
    rot_greasy: int
    """
    tongue_color: int
    coating_color: int
    tongue_thickness: int
    rot_greasy: int  


class Record(BaseModel):
    """
    ID: int
    user_ID: int
    img_src: str
    result: Result
    """
    ID: int
    user_ID: int
    img_src: str
    result: Result


class Upload(BaseModel):
    """
    fileData: str
    """
    fileData: str


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


class RecordResponse(BaseResponse):
    """
    code: int
    message: str
    data: List[Record]
    """
    data: list[Record]


class UploadResponse(BaseResponse):
    """
    code: int
    message: str
    data: {
        result: Result
    }
    """
    data: Union[Result, None]


class ExtendedOAuth2PasswordRequestForm:
    def __init__(
            self,
            *,
            email: Annotated[str, Form()],
            password: Annotated[str, Form()],
    ):
        self.email = email
        self.password = password
