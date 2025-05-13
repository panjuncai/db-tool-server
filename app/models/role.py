from app import db
from app.models.trm import trm

class Role(db.Model):
    __tablename__ = "t_role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    desc = db.Column(db.String(64))

    users = db.relationship('User', back_populates='role')
    menus = db.relationship('Menu', secondary=trm)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'menu': self.get_menu_dict()
        }

    def get_menu_dict(self):
        menu_list = []
        menus = sorted(self.menus, key=lambda temp: temp.id)
        for m in menus:
            if m.level == 1:
                first_dict = m.to_dict()
                first_dict['children'] = []
                for s in menus:
                    if s.level == 2 and s.pid == m.id:
                        first_dict['children'].append(s.to_dict())
                menu_list.append(first_dict)
        return menu_list