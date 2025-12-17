from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)  # 自增主键
    email = Column(String(255))
    password = Column(String(255))


class TongueAnalysis(Base):
    __tablename__ = 'TongueAnalysis'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    img_src = Column(String(255))
    state = Column(Integer)
    tongue_color = Column(Integer)
    coating_color = Column(Integer)
    tongue_thickness = Column(Integer)
    rot_greasy = Column(Integer)
    user = relationship('User')


class ChatSession(Base):
    __tablename__ = "chatSession"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    tittle = Column(String)
    user = relationship("User")
    chat_records = relationship("ChatRecord")


class ChatRecord(Base):
    __tablename__ = "chatRecord"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chatSession.id"))
    content = Column(String)
    create_at = Column(Integer, nullable=False)
    role = Column(Integer)
    session = relationship("ChatSession")
