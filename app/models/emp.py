from app import db
from app.models import BaseModel
from datetime import datetime

class Emp(db.Model, BaseModel):
    """员工表"""
    __tablename__ = 'emp'
    
    empno = db.Column(db.Integer, primary_key=True)  # 员工编号
    ename = db.Column(db.String(10))  # 员工姓名
    job = db.Column(db.String(9))  # 职位
    mgr = db.Column(db.Integer)  # 经理编号
    hiredate = db.Column(db.Date)  # 入职日期
    sal = db.Column(db.Numeric(7, 2))  # 薪水
    comm = db.Column(db.Numeric(7, 2))  # 佣金
    deptno = db.Column(db.Integer, db.ForeignKey('dept.deptno'))  # 部门编号
    
    def __repr__(self):
        return f'<Emp {self.ename}>'
    
    @classmethod
    def get_all(cls):
        """获取所有员工"""
        return cls.query.all()
    
    @classmethod
    def get_by_empno(cls, empno):
        """通过员工编号获取员工"""
        return cls.query.filter_by(empno=empno).first()
    
    @classmethod
    def get_by_deptno(cls, deptno):
        """通过部门编号获取员工"""
        return cls.query.filter_by(deptno=deptno).all()
    
    @classmethod
    def get_by_job(cls, job):
        """通过职位获取员工"""
        return cls.query.filter_by(job=job).all() 