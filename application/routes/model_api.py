import os
import time
from fastapi import APIRouter, Depends, UploadFile, Body, Form, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from tempfile import SpooledTemporaryFile
from .ollama_used import OllamaStreamChatter
from ..core import get_current_user
from ..models import schemas
from ..orm.database import get_db
from ..orm import write_event, write_result, get_record_by_location, get_chat_record, get_all_chat_id, get_result, create_new_session, create_new_chat_records
from ..config import Settings
from ..net.predict import TonguePredictor
from ..config import settings

router_tongue_analysis = APIRouter()

feature_map = {
    "Color of the tongue": {
        0: "Pale white tongue",
        1: "Light red tongue",
        2: "Red tongue",
        3: "Crimson tongue",
        4: "Bluish-purple tongue"
    },
    "Color of the tongue coating": {
        0: "White coating",
        1: "Yellow tongue coating",
        2: "Gray-black tongue coating"
    },
    "Thickness of the tongue": {
        0: "Thin",
        1: "Thick"
    },
    "Decay and putrefaction of the tongue": {
        0: "Putrefaction",
        1: "decay"
    }
}

def format_tongue_features(tongue_color,
                           coating_color,
                           tongue_thickness,
                           rot_greasy):
    try:
        features = [
            f"Color of the tongue: {feature_map['Color of the tongue'][tongue_color]}",
            f"Color of the tongue coating: {feature_map['Color of the tongue coating'][coating_color]}",
            f"Thickness of the tongue: {feature_map['Thickness of the tongue'][tongue_thickness]}",
            f"Decay and putrefaction of the tongue: {feature_map['Decay and putrefaction of the tongue'][rot_greasy]}"
        ]
        return "，".join(features)
    except KeyError as e:
        missing_key = int(str(e).split("'")[1])
        return f"错误：检测到无效特征值 {missing_key}，请检查输入范围"


class UserInput(BaseModel):
    input: str

@router_tongue_analysis.post('/session/{sessionId}')
async def upload(sessionId: int,
                 user_input: UserInput,
                 user: schemas.UserBase = Depends(get_current_user),
                 db: Session = Depends(get_db),
                 ):
    if not user:
        return schemas.BaseModel(
            code=101,
            message="can not find user",
            data=None
        )
    else:
        bot = OllamaStreamChatter(
            system_prompt=settings.SYSTEM_PROMPT
        )
        create_new_chat_records(db=db, content=user_input.input, session_id=sessionId, role=1)
        return bot.chat_stream_add(user.id, db, sessionId)


class inputPicture(BaseModel):
    file_data: UploadFile
    user_input: str
    name: str

@router_tongue_analysis.post('/session')
async def upload(file_data: UploadFile = File(...),
                user_input: str = Form(...),
                name: str = Form(...),
                 user: schemas.UserBase = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):
    if not user:
        return schemas.BaseModel(
            code=101,
            message="can not find user",
            data=None
        )

    def analysis(img: SpooledTemporaryFile, record_id: int, function):
        predictor = TonguePredictor()
        predictor.predict(img=img, record_id=record_id, fun=function)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file_data.filename)[1]
    filename = f"{timestamp}{file_extension}"
    file_location = f"{Settings.IMG_PATH}/{filename}"
    with open(file_location, "wb") as f:
        contents = await file_data.read()
        f.write(contents)
    f.close()

    img_db_path = f"{Settings.IMG_DB_PATH}/{filename}"
    code = write_event(user_id=user.id, img_src=img_db_path, state=0, db=db)

    if code == 0:
        record = get_record_by_location(img_db_path, db=db)
        analysis(img=file_data.file, record_id=record.id, function=write_result)
        while True:
            result1 = get_result(img_db_path, db=db)
            if result1.state != 0:
                break
            time.sleep(1)

        result = get_result(img_db_path, db=db)
        if result.state != 1:
            return schemas.BaseModel(
                code=result.state,
                message="图片有问题",
                data=None
            )
        tongue_color = result.tongue_color
        coating_color = result.coating_color
        tongue_thickness = result.tongue_thickness
        rot_greasy = result.rot_greasy
        feature = format_tongue_features(tongue_color,coating_color,tongue_thickness,rot_greasy)
        bot = OllamaStreamChatter(
            system_prompt=settings.SYSTEM_PROMPT
        )
        new_message = create_new_session(ID=user.id, db=db, tittle=name)
        session_new_id = new_message.id
        create_new_chat_records(db=db, content=user_input, session_id=session_new_id, role=1)
        return bot.chat_stream_first(user_input, feature, user.id, db, session_new_id)
    else:
        return schemas.UploadResponse(
            code=201,
            message="operation failed",
            data=None
        )

@router_tongue_analysis.get("/record/{sessionid}", response_model=schemas.ChatSessionRecordsResponse)
async def get_chat_records_by_session(sessionid: int,
                                      db: Session = Depends(get_db),
                                      user: schemas.UserBase = Depends(get_current_user)
                                      ):
    if not user:
        return schemas.ChatSessionRecordsResponse(
            code=101,
            message="can not find user",
            data={"records": []}
        )
    else:
        chat_record = get_chat_record(ID=user.id, sessionid=sessionid, db=db)
        if chat_record == 102 or chat_record == 103:
            return schemas.ChatSessionRecordsResponse(
                code=chat_record,
                message="operation failed",
                data={"records": []}
            )
        else:
            records = []
            for record in chat_record:
                records.append(schemas.ChatRecordResponse(
                    content=record.content,
                    create_at=record.create_at,
                    role=record.role
                ))
            data_temp = {
                "records": records
            }
            return schemas.ChatSessionRecordsResponse(
                code=0,
                message="operation success",
                data=data_temp,
            )

@router_tongue_analysis.get("/session", response_model=schemas.SessionIdResponse)
async def get_chat_records_id(db: Session = Depends(get_db),
                              user: schemas.UserBase = Depends(get_current_user)):
    if not user:
        return schemas.SessionIdResponse(
            code=101,
            message="can not find user",
            data=[]
        )
    else:
        chat_id_records = get_all_chat_id(ID=user.id, db=db)
        data_temp = []
        for record in chat_id_records:
            data_temp.append(schemas.SessionId(
                session_id=record.id,
                name=record.tittle
            ))
        return schemas.SessionIdResponse(
            code=0,
            message="operation success",
            data=data_temp
        )
