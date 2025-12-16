"""
定义数据库模型
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):  # 用户基本信息
    """
    CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255)
    );
   """
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)  # 自增主键
    email = Column(String(255))
    password = Column(String(255))


class TongueAnalysis(Base):
    """
    CREATE TABLE TongueAnalysis (
    id INT PRIMARY KEY,
    user_id INT,
    img_src VARCHAR(255),
    tongue_color Column(Integer),
    舌色：0:淡百舌，1:淡红舌，2:红舌，3:绛舌，4:青紫舌
    coating_color Column(Integer),
    舌苔颜色: 0:白苔，1:黄苔，2:灰黑苔
    tongue_thickness Column(Integer),
    厚薄：0:薄，1:厚
    rot_and_greasy Column(Integer),
    腐腻：0:腻，1:腐
    FOREIGN KEY (user_id) REFERENCES Users(id)
    );
    """
    __tablename__ = 'TongueAnalysis'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    img_src = Column(String(255))
    state = Column(Integer)
    tongue_color = Column(Integer)
    coating_color = Column(Integer)
    tongue_thickness = Column(Integer)
    rot_greasy = Column(Integer)
    # 定义与User表的外键关联关系
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