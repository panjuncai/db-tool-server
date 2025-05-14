from app import db
from app.models import BaseModel

class Bonus(db.Model, BaseModel):
    """奖金表"""
    __tablename__ = 'bonus'
    
    # 由于原表没有主键，这里添加一个自增ID作为主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ename = db.Column(db.String(10))  # 员工姓名
    job = db.Column(db.String(9))  # 职位
    sal = db.Column(db.Numeric)  # 薪水
    comm = db.Column(db.Numeric)  # 佣金
    
    def __repr__(self):
        return f'<Bonus {self.ename}>'
    
    @classmethod
    def get_all(cls):
        """获取所有奖金记录"""
        return cls.query.all()
    
    @classmethod
    def get_by_ename(cls, ename):
        """通过员工姓名获取奖金记录"""
        return cls.query.filter_by(ename=ename).all()
    
    @classmethod
    def get_by_job(cls, job):
        """通过职位获取奖金记录"""
        return cls.query.filter_by(job=job).all() 