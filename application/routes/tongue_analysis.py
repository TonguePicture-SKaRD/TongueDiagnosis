from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import schemas
from ..orm import analysis_tongue
from ..orm.database import get_db

router_tongue_analysis = APIRouter()


@router_tongue_analysis.post('/upload', response_model=schemas.TongueAnalysisResponse)
async def upload(fileData: schemas.TongueAnalysisPic, db: Session = Depends(get_db)):
    """
    上传舌头图片的路由
    @param fileData: TongueAnalysisPic
        fileData: file
    @param db: 路由传回的当前会话的db，获取数据库链接
    @return: TongueAnalysisResponse
        code: int
        message: str
        data: object
    """
    pass
