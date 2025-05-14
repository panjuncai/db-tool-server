from flask import Blueprint, jsonify, request
from app.models import Bonus
from app import db

bonus_bp = Blueprint('bonus', __name__, url_prefix='/api/bonus')

@bonus_bp.route('/', methods=['GET'])
def get_all_bonuses():
    """获取所有奖金记录"""
    bonuses = Bonus.get_all()
    return jsonify({
        'code': 200,
        'message': '获取奖金列表成功',
        'data': [
            {
                'id': bonus.id,
                'ename': bonus.ename,
                'job': bonus.job,
                'sal': float(bonus.sal) if bonus.sal else None,
                'comm': float(bonus.comm) if bonus.comm else None
            } for bonus in bonuses
        ]
    })

@bonus_bp.route('/ename/<string:ename>', methods=['GET'])
def get_bonuses_by_ename(ename):
    """获取指定员工的奖金记录"""
    bonuses = Bonus.get_by_ename(ename)
    return jsonify({
        'code': 200,
        'message': f'获取员工 {ename} 奖金记录成功',
        'data': [
            {
                'id': bonus.id,
                'ename': bonus.ename,
                'job': bonus.job,
                'sal': float(bonus.sal) if bonus.sal else None,
                'comm': float(bonus.comm) if bonus.comm else None
            } for bonus in bonuses
        ]
    })

@bonus_bp.route('/job/<string:job>', methods=['GET'])
def get_bonuses_by_job(job):
    """获取指定职位的奖金记录"""
    bonuses = Bonus.get_by_job(job)
    return jsonify({
        'code': 200,
        'message': f'获取职位 {job} 奖金记录成功',
        'data': [
            {
                'id': bonus.id,
                'ename': bonus.ename,
                'job': bonus.job,
                'sal': float(bonus.sal) if bonus.sal else None,
                'comm': float(bonus.comm) if bonus.comm else None
            } for bonus in bonuses
        ]
    })

@bonus_bp.route('/', methods=['POST'])
def create_bonus():
    """创建奖金记录"""
    data = request.get_json()
    
    if not all(key in data for key in ['ename', 'job']):
        return jsonify({
            'code': 400,
            'message': '缺少必要参数'
        }), 400
    
    bonus = Bonus(
        ename=data['ename'],
        job=data['job'],
        sal=data.get('sal'),
        comm=data.get('comm')
    )
    
    try:
        bonus.save()
        return jsonify({
            'code': 201,
            'message': '奖金记录创建成功',
            'data': {
                'id': bonus.id,
                'ename': bonus.ename,
                'job': bonus.job,
                'sal': float(bonus.sal) if bonus.sal else None,
                'comm': float(bonus.comm) if bonus.comm else None
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'奖金记录创建失败: {str(e)}'
        }), 500

@bonus_bp.route('/<int:id>', methods=['PUT'])
def update_bonus(id):
    """更新奖金记录"""
    bonus = Bonus.get_by_id(id)
    if not bonus:
        return jsonify({
            'code': 404,
            'message': f'奖金记录 ID {id} 不存在'
        }), 404
    
    data = request.get_json()
    
    if 'ename' in data:
        bonus.ename = data['ename']
    if 'job' in data:
        bonus.job = data['job']
    if 'sal' in data:
        bonus.sal = data['sal']
    if 'comm' in data:
        bonus.comm = data['comm']
    
    try:
        bonus.save()
        return jsonify({
            'code': 200,
            'message': '奖金记录更新成功',
            'data': {
                'id': bonus.id,
                'ename': bonus.ename,
                'job': bonus.job,
                'sal': float(bonus.sal) if bonus.sal else None,
                'comm': float(bonus.comm) if bonus.comm else None
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'奖金记录更新失败: {str(e)}'
        }), 500

@bonus_bp.route('/<int:id>', methods=['DELETE'])
def delete_bonus(id):
    """删除奖金记录"""
    bonus = Bonus.get_by_id(id)
    if not bonus:
        return jsonify({
            'code': 404,
            'message': f'奖金记录 ID {id} 不存在'
        }), 404
    
    try:
        bonus.delete()
        return jsonify({
            'code': 200,
            'message': '奖金记录删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'奖金记录删除失败: {str(e)}'
        }), 500 