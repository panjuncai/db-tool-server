from app import db
from app.models.trm import trm

class Menu(db.Model):
    __tablename__ = 't_menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    level = db.Column(db.Integer)
    path = db.Column(db.String(32))

    pid = db.Column(db.Integer, db.ForeignKey('t_menu.id'))
    children = db.relationship('Menu')
    roles = db.relationship('Role', secondary=trm)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'path': self.path,
            'pid': self.pid
        }

    def get_child_list(self):
        obj_child = self.children
        data = []
        for o in obj_child:
            data.append(o.to_dict())
        return data