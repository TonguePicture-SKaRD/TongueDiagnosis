from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=ReusableSession)
Base = declarative_base()
