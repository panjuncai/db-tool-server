from app import db
from app.models import BaseModel

class Salgrade(db.Model, BaseModel):
    """薪资等级表"""
    __tablename__ = 'salgrade'
    
    # 由于原表没有明确指定主键，这里使用grade作为主键
    grade = db.Column(db.Integer, primary_key=True)  # 等级
    losal = db.Column(db.Numeric)  # 最低薪资
    hisal = db.Column(db.Numeric)  # 最高薪资
    
    def __repr__(self):
        return f'<Salgrade {self.grade}>'
    
    @classmethod
    def get_all(cls):
        """获取所有薪资等级"""
        return cls.query.all()
    
    @classmethod
    def get_by_grade(cls, grade):
        """通过等级获取薪资范围"""
        return cls.query.filter_by(grade=grade).first()
    
    @classmethod
    def get_grade_by_sal(cls, sal):
        """通过薪资获取等级"""
        return cls.query.filter(cls.losal <= sal, cls.hisal >= sal).first() 