from flask import Blueprint, jsonify, request
from app.models import Emp, Dept
from app import db
from datetime import datetime

emp_bp = Blueprint('emp', __name__, url_prefix='/api/emp')

@emp_bp.route('/', methods=['GET'])
def get_all_emps():
    """获取所有员工"""
    emps = Emp.get_all()
    return jsonify({
        'code': 200,
        'message': '获取员工列表成功',
        'data': [
            {
                'empno': emp.empno,
                'ename': emp.ename,
                'job': emp.job,
                'mgr': emp.mgr,
                'hiredate': emp.hiredate.strftime('%Y-%m-%d') if emp.hiredate else None,
                'sal': float(emp.sal) if emp.sal else None,
                'comm': float(emp.comm) if emp.comm else None,
                'deptno': emp.deptno
            } for emp in emps
        ]
    })

@emp_bp.route('/<int:empno>', methods=['GET'])
def get_emp(empno):
    """获取指定员工"""
    emp = Emp.get_by_empno(empno)
    if not emp:
        return jsonify({
            'code': 404,
            'message': f'员工编号 {empno} 不存在'
        }), 404
    
    return jsonify({
        'code': 200,
        'message': '获取员工信息成功',
        'data': {
            'empno': emp.empno,
            'ename': emp.ename,
            'job': emp.job,
            'mgr': emp.mgr,
            'hiredate': emp.hiredate.strftime('%Y-%m-%d') if emp.hiredate else None,
            'sal': float(emp.sal) if emp.sal else None,
            'comm': float(emp.comm) if emp.comm else None,
            'deptno': emp.deptno
        }
    })

@emp_bp.route('/dept/<int:deptno>', methods=['GET'])
def get_emps_by_dept(deptno):
    """获取指定部门的所有员工"""
    # 检查部门是否存在
    dept = Dept.get_by_deptno(deptno)
    if not dept:
        return jsonify({
            'code': 404,
            'message': f'部门编号 {deptno} 不存在'
        }), 404
    
    emps = Emp.get_by_deptno(deptno)
    return jsonify({
        'code': 200,
        'message': f'获取部门 {deptno} 员工列表成功',
        'data': [
            {
                'empno': emp.empno,
                'ename': emp.ename,
                'job': emp.job,
                'mgr': emp.mgr,
                'hiredate': emp.hiredate.strftime('%Y-%m-%d') if emp.hiredate else None,
                'sal': float(emp.sal) if emp.sal else None,
                'comm': float(emp.comm) if emp.comm else None,
                'deptno': emp.deptno
            } for emp in emps
        ]
    })

@emp_bp.route('/job/<string:job>', methods=['GET'])
def get_emps_by_job(job):
    """获取指定职位的所有员工"""
    emps = Emp.get_by_job(job)
    return jsonify({
        'code': 200,
        'message': f'获取职位 {job} 员工列表成功',
        'data': [
            {
                'empno': emp.empno,
                'ename': emp.ename,
                'job': emp.job,
                'mgr': emp.mgr,
                'hiredate': emp.hiredate.strftime('%Y-%m-%d') if emp.hiredate else None,
                'sal': float(emp.sal) if emp.sal else None,
                'comm': float(emp.comm) if emp.comm else None,
                'deptno': emp.deptno
            } for emp in emps
        ]
    })

@emp_bp.route('/', methods=['POST'])
def create_emp():
    """创建员工"""
    data = request.get_json()
    
    if not all(key in data for key in ['empno', 'ename', 'job', 'deptno']):
        return jsonify({
            'code': 400,
            'message': '缺少必要参数'
        }), 400
    
    # 检查员工编号是否已存在
    existing_emp = Emp.get_by_empno(data['empno'])
    if existing_emp:
        return jsonify({
            'code': 400,
            'message': f'员工编号 {data["empno"]} 已存在'
        }), 400
    
    # 检查部门是否存在
    dept = Dept.get_by_deptno(data['deptno'])
    if not dept:
        return jsonify({
            'code': 400,
            'message': f'部门编号 {data["deptno"]} 不存在'
        }), 400
    
    # 处理日期格式
    hiredate = None
    if 'hiredate' in data and data['hiredate']:
        try:
            hiredate = datetime.strptime(data['hiredate'], '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': '日期格式错误，应为 YYYY-MM-DD'
            }), 400
    
    emp = Emp(
        empno=data['empno'],
        ename=data['ename'],
        job=data['job'],
        mgr=data.get('mgr'),
        hiredate=hiredate,
        sal=data.get('sal'),
        comm=data.get('comm'),
        deptno=data['deptno']
    )
    
    try:
        emp.save()
        return jsonify({
            'code': 201,
            'message': '员工创建成功',
            'data': {
                'empno': emp.empno,
                'ename': emp.ename,
                'job': emp.job,
                'mgr': emp.mgr,
                'hiredate': emp.hiredate.strftime('%Y-%m-%d') if emp.hiredate else None,
                'sal': float(emp.sal) if emp.sal else None,
                'comm': float(emp.comm) if emp.comm else None,
                'deptno': emp.deptno
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'员工创建失败: {str(e)}'
        }), 500

@emp_bp.route('/<int:empno>', methods=['PUT'])
def update_emp(empno):
    """更新员工信息"""
    emp = Emp.get_by_empno(empno)
    if not emp:
        return jsonify({
            'code': 404,
            'message': f'员工编号 {empno} 不存在'
        }), 404
    
    data = request.get_json()
    
    if 'ename' in data:
        emp.ename = data['ename']
    if 'job' in data:
        emp.job = data['job']
    if 'mgr' in data:
        emp.mgr = data['mgr']
    if 'hiredate' in data and data['hiredate']:
        try:
            emp.hiredate = datetime.strptime(data['hiredate'], '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': '日期格式错误，应为 YYYY-MM-DD'
            }), 400
    if 'sal' in data:
        emp.sal = data['sal']
    if 'comm' in data:
        emp.comm = data['comm']
    if 'deptno' in data:
        # 检查部门是否存在
        dept = Dept.get_by_deptno(data['deptno'])
        if not dept:
            return jsonify({
                'code': 400,
                'message': f'部门编号 {data["deptno"]} 不存在'
            }), 400
        emp.deptno = data['deptno']
    
    try:
        emp.save()
        return jsonify({
            'code': 200,
            'message': '员工更新成功',
            'data': {
                'empno': emp.empno,
                'ename': emp.ename,
                'job': emp.job,
                'mgr': emp.mgr,
                'hiredate': emp.hiredate.strftime('%Y-%m-%d') if emp.hiredate else None,
                'sal': float(emp.sal) if emp.sal else None,
                'comm': float(emp.comm) if emp.comm else None,
                'deptno': emp.deptno
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'员工更新失败: {str(e)}'
        }), 500

@emp_bp.route('/<int:empno>', methods=['DELETE'])
def delete_emp(empno):
    """删除员工"""
    emp = Emp.get_by_empno(empno)
    if not emp:
        return jsonify({
            'code': 404,
            'message': f'员工编号 {empno} 不存在'
        }), 404
    
    try:
        emp.delete()
        return jsonify({
            'code': 200,
            'message': '员工删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'员工删除失败: {str(e)}'
        }), 500 