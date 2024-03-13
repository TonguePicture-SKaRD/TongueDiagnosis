from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


# 重写Session类，使其提交失败时自动回滚
class ReusableSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def commit(self):
        try:
            super().commit()
        except Exception as e:
            self.rollback()
            raise e


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_object():
    return SessionLocal()


engine = create_engine('sqlite:///AppDatabase.db')
# 将ReusableSession作为session maker的class参数传入，使其创建的Session自动回滚
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=ReusableSession)
Base = declarative_base()
