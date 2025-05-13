from app import db

trm = db.Table('t_role_menu',
               db.Column('rid', db.Integer, db.ForeignKey('t_role.id')),
               db.Column('mid', db.Integer, db.ForeignKey('t_menu.id'))
               )