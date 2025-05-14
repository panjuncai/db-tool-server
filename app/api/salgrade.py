from flask import Blueprint, jsonify, request
from app.models import Salgrade
from app import db

salgrade_bp = Blueprint('salgrade', __name__, url_prefix='/api/salgrade')

@salgrade_bp.route('/', methods=['GET'])
def get_all_salgrades():
    """获取所有薪资等级"""
    salgrades = Salgrade.get_all()
    return jsonify({
        'code': 200,
        'message': '获取薪资等级列表成功',
        'data': [
            {
                'grade': salgrade.grade,
                'losal': float(salgrade.losal) if salgrade.losal else None,
                'hisal': float(salgrade.hisal) if salgrade.hisal else None
            } for salgrade in salgrades
        ]
    })

@salgrade_bp.route('/<int:grade>', methods=['GET'])
def get_salgrade(grade):
    """获取指定等级的薪资范围"""
    salgrade = Salgrade.get_by_grade(grade)
    if not salgrade:
        return jsonify({
            'code': 404,
            'message': f'薪资等级 {grade} 不存在'
        }), 404
    
    return jsonify({
        'code': 200,
        'message': '获取薪资等级信息成功',
        'data': {
            'grade': salgrade.grade,
            'losal': float(salgrade.losal) if salgrade.losal else None,
            'hisal': float(salgrade.hisal) if salgrade.hisal else None
        }
    })

@salgrade_bp.route('/sal/<float:sal>', methods=['GET'])
def get_grade_by_sal(sal):
    """通过薪资获取等级"""
    salgrade = Salgrade.get_grade_by_sal(sal)
    if not salgrade:
        return jsonify({
            'code': 404,
            'message': f'没有匹配薪资 {sal} 的等级'
        }), 404
    
    return jsonify({
        'code': 200,
        'message': '获取薪资等级信息成功',
        'data': {
            'grade': salgrade.grade,
            'losal': float(salgrade.losal) if salgrade.losal else None,
            'hisal': float(salgrade.hisal) if salgrade.hisal else None
        }
    })

@salgrade_bp.route('/', methods=['POST'])
def create_salgrade():
    """创建薪资等级"""
    data = request.get_json()
    
    if not all(key in data for key in ['grade', 'losal', 'hisal']):
        return jsonify({
            'code': 400,
            'message': '缺少必要参数'
        }), 400
    
    # 检查等级是否已存在
    existing_salgrade = Salgrade.get_by_grade(data['grade'])
    if existing_salgrade:
        return jsonify({
            'code': 400,
            'message': f'薪资等级 {data["grade"]} 已存在'
        }), 400
    
    # 检查薪资范围是否合理
    if float(data['losal']) > float(data['hisal']):
        return jsonify({
            'code': 400,
            'message': '最低薪资不能大于最高薪资'
        }), 400
    
    salgrade = Salgrade(
        grade=data['grade'],
        losal=data['losal'],
        hisal=data['hisal']
    )
    
    try:
        salgrade.save()
        return jsonify({
            'code': 201,
            'message': '薪资等级创建成功',
            'data': {
                'grade': salgrade.grade,
                'losal': float(salgrade.losal) if salgrade.losal else None,
                'hisal': float(salgrade.hisal) if salgrade.hisal else None
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'薪资等级创建失败: {str(e)}'
        }), 500

@salgrade_bp.route('/<int:grade>', methods=['PUT'])
def update_salgrade(grade):
    """更新薪资等级信息"""
    salgrade = Salgrade.get_by_grade(grade)
    if not salgrade:
        return jsonify({
            'code': 404,
            'message': f'薪资等级 {grade} 不存在'
        }), 404
    
    data = request.get_json()
    
    if 'losal' in data:
        salgrade.losal = data['losal']
    if 'hisal' in data:
        salgrade.hisal = data['hisal']
    
    # 检查薪资范围是否合理
    if float(salgrade.losal) > float(salgrade.hisal):
        return jsonify({
            'code': 400,
            'message': '最低薪资不能大于最高薪资'
        }), 400
    
    try:
        salgrade.save()
        return jsonify({
            'code': 200,
            'message': '薪资等级更新成功',
            'data': {
                'grade': salgrade.grade,
                'losal': float(salgrade.losal) if salgrade.losal else None,
                'hisal': float(salgrade.hisal) if salgrade.hisal else None
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'薪资等级更新失败: {str(e)}'
        }), 500

@salgrade_bp.route('/<int:grade>', methods=['DELETE'])
def delete_salgrade(grade):
    """删除薪资等级"""
    salgrade = Salgrade.get_by_grade(grade)
    if not salgrade:
        return jsonify({
            'code': 404,
            'message': f'薪资等级 {grade} 不存在'
        }), 404
    
    try:
        salgrade.delete()
        return jsonify({
            'code': 200,
            'message': '薪资等级删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'薪资等级删除失败: {str(e)}'
        }), 500 