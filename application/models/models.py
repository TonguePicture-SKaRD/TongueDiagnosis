from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):  # 用户基本信息
    """
        table:
            create table users (
                id int primary key auto_increment,
                email varchar(255) unique not null,
                password varchar(255) not null,
            );
    """
    __tableName__ = 'User'
    id = Column(Integer, primary_key=True)  # 自增主键
    email = Column(String(255))
    password = Column(String(255))
