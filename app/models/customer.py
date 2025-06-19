from app import db
from datetime import datetime

class Customer(db.Model):
    """客户表"""
    __tablename__ = 'customers'
    
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(50))
    contact_title = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    credit_limit = db.Column(db.Numeric(12, 2))
    credit_rating = db.Column(db.String(10))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(10), default='ACTIVE')
    industry = db.Column(db.String(50))
    annual_revenue = db.Column(db.Numeric(15, 2))
    employee_count = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Customer {self.company_name}>'
    
    def save(self):
        """保存当前记录"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """删除当前记录"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_all(cls):
        """获取所有客户"""
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, customer_id):
        """通过客户ID获取客户"""
        return cls.query.filter_by(customer_id=customer_id).first()
    
    @classmethod
    def get_by_company_name(cls, company_name):
        """通过公司名称获取客户"""
        return cls.query.filter_by(company_name=company_name).first()
    
    @classmethod
    def get_by_status(cls, status):
        """通过状态获取客户"""
        return cls.query.filter_by(status=status).all()
    
    @classmethod
    def get_by_credit_rating(cls, credit_rating):
        """通过信用评级获取客户"""
        return cls.query.filter_by(credit_rating=credit_rating).all()
    
    @classmethod
    def get_by_city(cls, city):
        """通过城市获取客户"""
        return cls.query.filter_by(city=city).all()
    
    @classmethod
    def get_by_industry(cls, industry):
        """通过行业获取客户"""
        return cls.query.filter_by(industry=industry).all()
    
    @classmethod
    def search_by_name(cls, keyword):
        """通过关键词搜索客户（公司名称或联系人姓名）"""
        return cls.query.filter(
            (cls.company_name.contains(keyword)) |
            (cls.contact_name.contains(keyword))
        ).all()
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'customer_id': self.customer_id,
            'company_name': self.company_name,
            'contact_name': self.contact_name,
            'contact_title': self.contact_title,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'credit_limit': float(self.credit_limit) if self.credit_limit else None,
            'credit_rating': self.credit_rating,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S') if self.created_date else None,
            'last_modified': self.last_modified.strftime('%Y-%m-%d %H:%M:%S') if self.last_modified else None,
            'status': self.status,
            'industry': self.industry,
            'annual_revenue': float(self.annual_revenue) if self.annual_revenue else None,
            'employee_count': self.employee_count
        } 