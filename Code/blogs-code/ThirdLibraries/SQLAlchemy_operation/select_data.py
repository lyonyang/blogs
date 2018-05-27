#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author：Lyon
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Index, UniqueConstraint
from sqlalchemy.orm import sessionmaker
# 根据Dialet创建引擎,echo=True表示输出所有操作日志
engine = create_engine('mysql+pymysql://root:myroot@localhost:3306/test', echo=False)
# 声明基类
Base = declarative_base()
# 定义映射类
class Userinfo(Base):
    # 表名
    __tablename__ = 'userinfo'
    # 设置主键自增列
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    extra = Column(String(16))
    __table_args__ = (
        # 唯一索引,索引名为uix_id_name
    	UniqueConstraint('id', 'name', name='uix_id_name'),
        # 联合索引
        Index('ix_id_name', 'name', 'extra'),
    )
    # 定义格式
    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)
Session = sessionmaker(bind=engine)
# 创建Session实例
session = Session()
# 查所有,取所有字段
res = session.query(Userinfo).all()
print(res)
# 查所有,取指定字段,按照id排序
res = session.query(Userinfo.name).order_by(Userinfo.id).all()
print(res)
# 查所有,取指定字段,第一条信息
res = session.query(Userinfo.name).first()
print(res)
# 过滤查,逗号分隔,默认为and
res = session.query(Userinfo).filter(Userinfo.id > 1,Userinfo.id <1000)
print([(row.id, row.name) for row in res], type(res))
ret = session.query(Users).filter_by(name='alex').all()
session.commit()