import os
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from tempfile import SpooledTemporaryFile

from ..core import get_current_user
from ..models import schemas
from ..orm.database import get_db
from ..orm import write_event, write_result, get_record_by_location, get_chat_record, get_all_chat_id
from ..config import Settings

from ..net.predict import TonguePredictor

router_tongue_analysis = APIRouter()

@router_tongue_analysis.post('/session', response_model=schemas.UploadResponse)
async def upload(file_data: UploadFile,
                 user: schemas.UserBase = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):
    """
    上传舌头图片的路由
    @param file_data: schemas.Upload
        fileData: UploadFile
    @param user: User，当前用户信息
    @param db: 路由传回的当前会话的db，获取数据库链接
    @return: TongueAnalysisResponse
        code: int  # 0表示图片上传成功，201表示图片上传失败
        message: str
    """

    # 模型分析
    def analysis(img: SpooledTemporaryFile, record_id: int, function):
        """
        模型分析
        :param img: 图片
        :param record_id: 事件id
        :param function: 保存结果的函数
        :return: None
        """
        predictor = TonguePredictor()
        predictor.predict(img=img, record_id=record_id, fun=function)

    # 保存图片
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file_data.filename)[1]
    filename = f"{timestamp}{file_extension}"
    file_location = f"{Settings.IMG_PATH}/{filename}"
    with open(file_location, "wb") as f:
        contents = await file_data.read()
        f.write(contents)
    f.close()

    # 写入事件
    img_db_path = f"{Settings.IMG_DB_PATH}/{filename}"
    code = write_event(user_id=user.id, img_src=img_db_path, state=0, db=db)

    # 模型调用
    if code == 0:  #成果分析结果
        record = get_record_by_location(img_db_path, db=db)
        analysis(img=file_data.file, record_id=record.id, function=write_result)
        return schemas.UploadResponse(
            code=0,
            message="operation success",
            data=None
        )
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
    """
    获取用户的指定的对话记录
    :param sessionid: int
    :param db: Session, router传入的db，用于链接数据库
    :param user: User
    :return: ChatSessionRecordsResponse
    """
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
                if isinstance(record.create_at, datetime):
                    timestamp = int(record.create_at.timestamp())
                else:
                    timestamp = None  # 如果 create_at 不是有效的 datetime，设置为 None 或默认值

                records.append(schemas.ChatRecordResponse(
                    content=record.content,
                    create_at=timestamp,
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
                name=record.title
            ))
        return schemas.SessionIdResponse(
            code=0,
            message="operation success",
            data=data_temp
        )

