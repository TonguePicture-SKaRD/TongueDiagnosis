import time
from pydantic import BaseModel,Field
from typing import Union, Annotated, Optional
from fastapi.param_functions import Form
from typing import List


class BaseResponse(BaseModel):
    code: int
    message: str
    data: Union[dict, list] = None


class Token(BaseModel):
    token: str


class UserBase(BaseModel):
    ID: int = None
    email: str


class UserAuth(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(BaseModel):
    email: str
    password: str


class Result(BaseModel):
    tongue_color: Optional[int] = None
    coating_color: Optional[int] = None
    tongue_thickness: Optional[int] = None
    rot_greasy: Optional[int] = None


class Record(BaseModel):
    ID: int
    user_ID: int
    img_src: str
    state: int = None
    result: Optional[Result] = None


class LoginResponse(BaseResponse):
    data: Union[Token, None]


class RegisterResponse(BaseResponse):
    pass


class InfoResponse(BaseResponse):
    data: Union[UserBase, None]


class RecordResponse(BaseResponse):
    data: list[Record]


class UploadResponse(BaseResponse):
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
