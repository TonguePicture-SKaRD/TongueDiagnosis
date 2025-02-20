"""
这个文件包含了所有的请求和响应的Pydantic模型
供后续的API路由使用
"""
import time

from pydantic import BaseModel,Field
from typing import Union, Annotated, Optional
from fastapi.param_functions import Form
from typing import List


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
    tongue_color: Optional[int] = None
    coating_color: Optional[int] = None
    tongue_thickness: Optional[int] = None
    rot_greasy: Optional[int] = None


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
    state: int = None
    result: Optional[Result] = None


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
    data: None
    """
    data: None


class ExtendedOAuth2PasswordRequestForm:
    def __init__(
            self,
            *,
            email: Annotated[str, Form()],
            password: Annotated[str, Form()],
    ):
        self.email = email
        self.password = password


class ChatRecordResponse(BaseModel):
    content: str
    create_at: int = Field(default_factory=lambda: int(time.time() * 1000))
    role: int

class ChatSessionRecordsResponse(BaseModel):
    code: int
    message: str
    data: dict[str, List[ChatRecordResponse]]

class SessionId(BaseModel):
    session_id: int
    name: str

class SessionIdResponse(BaseModel):
    code: int
    message: str
    data: List[SessionId]