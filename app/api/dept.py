from flask import Blueprint, jsonify, request
from app.models import Dept
from app import db

dept_bp = Blueprint('dept', __name__, url_prefix='/api/dept')

@dept_bp.route('/', methods=['GET'])
def get_all_depts():
    """获取所有部门"""
    depts = Dept.get_all()
    return jsonify({
        'code': 200,
        'message': '获取部门列表成功',
        'data': [
            {
                'deptno': dept.deptno,
                'dname': dept.dname,
                'loc': dept.loc
            } for dept in depts
        ]
    })

@dept_bp.route('/<int:deptno>', methods=['GET'])
def get_dept(deptno):
    """获取指定部门"""
    dept = Dept.get_by_deptno(deptno)
    if not dept:
        return jsonify({
            'code': 404,
            'message': f'部门编号 {deptno} 不存在'
        }), 404
    
    return jsonify({
        'code': 200,
        'message': '获取部门信息成功',
        'data': {
            'deptno': dept.deptno,
            'dname': dept.dname,
            'loc': dept.loc
        }
    })

@dept_bp.route('/', methods=['POST'])
def create_dept():
    """创建部门"""
    data = request.get_json()
    
    if not all(key in data for key in ['deptno', 'dname']):
        return jsonify({
            'code': 400,
            'message': '缺少必要参数'
        }), 400
    
    # 检查部门编号是否已存在
    existing_dept = Dept.get_by_deptno(data['deptno'])
    if existing_dept:
        return jsonify({
            'code': 400,
            'message': f'部门编号 {data["deptno"]} 已存在'
        }), 400
    
    dept = Dept(
        deptno=data['deptno'],
        dname=data['dname'],
        loc=data.get('loc', '')
    )
    
    try:
        dept.save()
        return jsonify({
            'code': 201,
            'message': '部门创建成功',
            'data': {
                'deptno': dept.deptno,
                'dname': dept.dname,
                'loc': dept.loc
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'部门创建失败: {str(e)}'
        }), 500

@dept_bp.route('/<int:deptno>', methods=['PUT'])
def update_dept(deptno):
    """更新部门信息"""
    dept = Dept.get_by_deptno(deptno)
    if not dept:
        return jsonify({
            'code': 404,
            'message': f'部门编号 {deptno} 不存在'
        }), 404
    
    data = request.get_json()
    
    if 'dname' in data:
        dept.dname = data['dname']
    if 'loc' in data:
        dept.loc = data['loc']
    
    try:
        dept.save()
        return jsonify({
            'code': 200,
            'message': '部门更新成功',
            'data': {
                'deptno': dept.deptno,
                'dname': dept.dname,
                'loc': dept.loc
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'部门更新失败: {str(e)}'
        }), 500

@dept_bp.route('/<int:deptno>', methods=['DELETE'])
def delete_dept(deptno):
    """删除部门"""
    dept = Dept.get_by_deptno(deptno)
    if not dept:
        return jsonify({
            'code': 404,
            'message': f'部门编号 {deptno} 不存在'
        }), 404
    
    try:
        dept.delete()
        return jsonify({
            'code': 200,
            'message': '部门删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'部门删除失败: {str(e)}'
        }), 500 