#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Index, UniqueConstraint
engine = create_engine('mysql+pymysql://root:myroot@localhost:3306/test', echo=True)  # echo=True输出生成的SQL语句
Base = declarative_base()
class UserInfo(Base):
    __tablename__ = 'UserInfo'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)  # primary_key=主键,autoincrement=自增
    name = Column(String(32))
    extra = Column(String(16))
    __table_args__ = (
    UniqueConstraint('id', 'name', name='uix_id_name'),
        Index('ix_id_name', 'name', 'extra'),
    )
    # 让查询出来的数据显示中文
    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)
def init_db():
    Base.metadata.create_all(engine)
init_db()