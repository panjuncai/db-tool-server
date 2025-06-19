from flask import Blueprint, jsonify, request
from app.models import Customer
from app import db
from datetime import datetime

customer_bp = Blueprint('customer', __name__, url_prefix='/api/customer')

@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    """All customers"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    credit_rating = request.args.get('credit_rating')
    city = request.args.get('city')
    industry = request.args.get('industry')
    search = request.args.get('search')
    
    query = Customer.query
    
    # 添加过滤条件
    if status:
        query = query.filter_by(status=status)
    if credit_rating:
        query = query.filter_by(credit_rating=credit_rating)
    if city:
        query = query.filter_by(city=city)
    if industry:
        query = query.filter_by(industry=industry)
    if search:
        query = query.filter(
            (Customer.company_name.contains(search)) |
            (Customer.contact_name.contains(search))
        )
    
    # 分页查询
    customers_pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    customers = customers_pagination.items
    
    return jsonify({
        'code': 200,
        'message': '获取客户列表成功',
        'data': {
            'customers': [customer.to_dict() for customer in customers],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': customers_pagination.total,
                'pages': customers_pagination.pages,
                'has_next': customers_pagination.has_next,
                'has_prev': customers_pagination.has_prev
            }
        }
    })

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """获取指定客户"""
    customer = Customer.get_by_id(customer_id)
    if not customer:
        return jsonify({
            'code': 404,
            'message': f'客户ID {customer_id} 不存在'
        }), 404
    
    return jsonify({
        'code': 200,
        'message': '获取客户信息成功',
        'data': customer.to_dict()
    })

@customer_bp.route('/search', methods=['GET'])
def search_customers():
    """Search customers"""
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({
            'code': 400,
            'message': 'Please provide a search keyword'
        }), 400
    
    customers = Customer.search_by_name(keyword)
    return jsonify({
        'code': 200,
        'message': f'Search customers successfully, found {len(customers)} records',
        'data': [customer.to_dict() for customer in customers]
    })

@customer_bp.route('/status/<status>', methods=['GET'])
def get_customers_by_status(status):
    """Get customers by status"""
    if status not in ['ACTIVE', 'INACTIVE']:
        return jsonify({
            'code': 400,
            'message': 'Status must be ACTIVE or INACTIVE'
        }), 400
    
    customers = Customer.get_by_status(status)
    return jsonify({
        'code': 200,
        'message': f'Get customers by status {status} successfully',
        'data': [customer.to_dict() for customer in customers]
    })

@customer_bp.route('/credit-rating/<rating>', methods=['GET'])
def get_customers_by_credit_rating(rating):
    """Get customers by credit rating"""
    if rating not in ['A', 'B', 'C', 'D']:
        return jsonify({
            'code': 400,
            'message': 'Credit rating must be A, B, C or D'
        }), 400
    
    customers = Customer.get_by_credit_rating(rating)
    return jsonify({
        'code': 200,
        'message': f'Get customers by credit rating {rating} successfully',
        'data': [customer.to_dict() for customer in customers]
    })

@customer_bp.route('/city/<city>', methods=['GET'])
def get_customers_by_city(city):
    """Get customers by city"""
    customers = Customer.get_by_city(city)
    return jsonify({
        'code': 200,
        'message': f'Get customers by city {city} successfully',
        'data': [customer.to_dict() for customer in customers]
    })

@customer_bp.route('/industry/<industry>', methods=['GET'])
def get_customers_by_industry(industry):
    """Get customers by industry"""
    customers = Customer.get_by_industry(industry)
    return jsonify({
        'code': 200,
        'message': f'Get customers by industry {industry} successfully',
        'data': [customer.to_dict() for customer in customers]
    })

@customer_bp.route('/', methods=['POST'])
def create_customer():
    """ Create customer"""
    data = request.get_json()
    
    if not data.get('company_name'):
        return jsonify({
            'code': 400,
            'message': 'Company name cannot be empty'
        }), 400
    
    # 检查公司名称是否已存在
    existing_customer = Customer.get_by_company_name(data['company_name'])
    if existing_customer:
        return jsonify({
            'code': 400,
            'message': f'Company name {data["company_name"]} already exists'
        }), 400
    
    # 验证信用评级
    if data.get('credit_rating') and data['credit_rating'] not in ['A', 'B', 'C', 'D']:
        return jsonify({
            'code': 400,
            'message': 'Credit rating must be A, B, C or D'
        }), 400
    
    # 验证状态
    if data.get('status') and data['status'] not in ['ACTIVE', 'INACTIVE']:
        return jsonify({
            'code': 400,
            'message': 'Status must be ACTIVE or INACTIVE'
        }), 400
    
    customer = Customer(
        company_name=data['company_name'],
        contact_name=data.get('contact_name'),
        contact_title=data.get('contact_title'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        city=data.get('city'),
        country=data.get('country'),
        credit_limit=data.get('credit_limit'),
        credit_rating=data.get('credit_rating'),
        status=data.get('status', 'ACTIVE'),
        industry=data.get('industry'),
        annual_revenue=data.get('annual_revenue'),
        employee_count=data.get('employee_count')
    )
    
    try:
        customer.save()
        return jsonify({
            'code': 201,
            'message': 'Customer created successfully',
            'data': customer.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'Customer creation failed: {str(e)}'
        }), 500

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update customer information"""
    customer = Customer.get_by_id(customer_id)
    if not customer:
        return jsonify({
            'code': 404,
            'message': f'Customer ID {customer_id} does not exist'
        }), 404
    
    data = request.get_json()
    
    # 验证信用评级
    if data.get('credit_rating') and data['credit_rating'] not in ['A', 'B', 'C', 'D']:
        return jsonify({
            'code': 400,
            'message': 'Credit rating must be A, B, C or D'
        }), 400
    
    # 验证状态
    if data.get('status') and data['status'] not in ['ACTIVE', 'INACTIVE']:
        return jsonify({
            'code': 400,
            'message': 'Status must be ACTIVE or INACTIVE'
        }), 400
    
    # 更新字段
    if 'company_name' in data:
        # 检查新的公司名称是否已存在（排除当前客户）
        existing_customer = Customer.get_by_company_name(data['company_name'])
        if existing_customer and existing_customer.customer_id != customer_id:
            return jsonify({
                'code': 400,
                'message': f'Company name {data["company_name"]} already exists'
            }), 400
        customer.company_name = data['company_name']
    
    if 'contact_name' in data:
        customer.contact_name = data['contact_name']
    if 'contact_title' in data:
        customer.contact_title = data['contact_title']
    if 'phone' in data:
        customer.phone = data['phone']
    if 'email' in data:
        customer.email = data['email']
    if 'address' in data:
        customer.address = data['address']
    if 'city' in data:
        customer.city = data['city']
    if 'country' in data:
        customer.country = data['country']
    if 'credit_limit' in data:
        customer.credit_limit = data['credit_limit']
    if 'credit_rating' in data:
        customer.credit_rating = data['credit_rating']
    if 'status' in data:
        customer.status = data['status']
    if 'industry' in data:
        customer.industry = data['industry']
    if 'annual_revenue' in data:
        customer.annual_revenue = data['annual_revenue']
    if 'employee_count' in data:
        customer.employee_count = data['employee_count']
    
    # 更新最后修改时间
    customer.last_modified = datetime.utcnow()
    
    try:
        customer.save()
        return jsonify({
            'code': 200,
            'message': 'Customer updated successfully',
            'data': customer.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'Customer update failed: {str(e)}'
        }), 500

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete customer"""
    customer = Customer.get_by_id(customer_id)
    if not customer:
        return jsonify({
            'code': 404,
            'message': f'Customer ID {customer_id} does not exist'
        }), 404
    
    try:
        customer.delete()
        return jsonify({
            'code': 200,
            'message': 'Customer deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'Customer deletion failed: {str(e)}'
        }), 500

@customer_bp.route('/stats', methods=['GET'])
def get_customer_stats():
    """获取客户统计信息"""
    total_customers = Customer.query.count()
    active_customers = Customer.query.filter_by(status='ACTIVE').count()
    inactive_customers = Customer.query.filter_by(status='INACTIVE').count()
    
    # 按信用评级统计
    credit_stats = {}
    for rating in ['A', 'B', 'C', 'D']:
        credit_stats[rating] = Customer.query.filter_by(credit_rating=rating).count()
    
    # 按城市统计前10
    city_stats = db.session.query(
        Customer.city, 
        db.func.count(Customer.customer_id).label('count')
    ).filter(Customer.city.isnot(None)).group_by(Customer.city).order_by(
        db.func.count(Customer.customer_id).desc()
    ).limit(10).all()
    
    # 按行业统计前10
    industry_stats = db.session.query(
        Customer.industry,
        db.func.count(Customer.customer_id).label('count')
    ).filter(Customer.industry.isnot(None)).group_by(Customer.industry).order_by(
        db.func.count(Customer.customer_id).desc()
    ).limit(10).all()
    
    return jsonify({
        'code': 200,
        'message': 'Get customer stats successfully',
        'data': {
            'total_customers': total_customers,
            'active_customers': active_customers,
            'inactive_customers': inactive_customers,
            'credit_rating_stats': credit_stats,
            'top_cities': [{'city': city, 'count': count} for city, count in city_stats],
            'top_industries': [{'industry': industry, 'count': count} for industry, count in industry_stats]
        }
    }) 