from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///AppDatabase.db')  # 创建数据库引擎
SessionLocal = sessionmaker(bind=engine)  # 创建一个Session类
Base = declarative_base()  # 定义一个基类

# Base.metadata.create_all(engine)  # 创建基于Base的表结构
# db = SessionLocal()  # 创建一个Session实例
