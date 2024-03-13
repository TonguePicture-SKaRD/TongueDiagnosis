"""
数据库引擎与ORM搭建
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///AppDatabase.db')  # 创建数据库引擎
SessionLocal = sessionmaker(bind=engine)  # 创建一个Session类
Base = declarative_base()  # 定义一个基类
