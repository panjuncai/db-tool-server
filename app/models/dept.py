from app import db
from app.models import BaseModel

class Dept(db.Model, BaseModel):
    """部门表"""
    __tablename__ = 'dept'
    
    deptno = db.Column(db.Integer, primary_key=True)  # 部门编号
    dname = db.Column(db.String(14))  # 部门名称
    loc = db.Column(db.String(13))  # 部门位置
    
    # 与员工表的关系
    employees = db.relationship('Emp', backref='department', lazy='dynamic')
    
    def __repr__(self):
        return f'<Dept {self.dname}>'
    
    @classmethod
    def get_all(cls):
        """获取所有部门"""
        return cls.query.all()
    
    @classmethod
    def get_by_deptno(cls, deptno):
        """通过部门编号获取部门"""
        return cls.query.filter_by(deptno=deptno).first() 