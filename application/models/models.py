from sqlalchemy import Column, Integer, String
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
    tongue_color ENUM(''),
    coating_color ENUM(''),
    tongue_thickness ENUM(''),
    rot_and_greasy ENUM(''),
    FOREIGN KEY (user_id) REFERENCES Users(id)
    );
    """
    pass
