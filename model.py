from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Init for main app
def db_init(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    return db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='user', foreign_keys=[role_id])

    def __repr__(self):
        return f'{self.name}'

    def format(self):
        return({
            'id':self.id,
            'name':self.name,
            'phone':self.phone,
            'role_id':self.role_id
        })

class Table(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='table', foreign_keys=[owner_id])

    def __repr__(self):
        return f'{self.name}'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    privileges = db.relationship('Privilege', secondary='role_has_privilege', back_populates='roles')
    table_constraint = db.relationship('Privilege', secondary='table_relation_role', back_populates='roles')

    def __repr__(self):
        return f'{self.name}'

    def format(self):
        return({
            'id':self.id,
            'name':self.name,
            'description':self.description
        })

class Privilege(db.Model):
    __tablename__ = 'privileges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.Enum('account','relation'), nullable=False, server_default="account")

    roles = db.relationship('Role', secondary='role_has_privilege', back_populates='privileges')
    table_constraint = db.relationship('Role', secondary='table_relation_role', back_populates='privileges')

    def __repr__(self):
        return f'{self.name}'

    def format(self):
        return({
            'id':self.id,
            'name':self.name,
            'type':self.type
        })

class RoleHasPrivilege(db.Model):
    __tablename__ = 'role_has_privilege'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))
    privilege_id = db.Column(db.Integer, db.ForeignKey('privileges.id', ondelete='CASCADE'))

    role = db.relationship('Role', backref='role', foreign_keys=[role_id])
    privilege = db.relationship('Privilege', backref='previlege', foreign_keys=[privilege_id])

class TableConstraint(db.Model):
    __tablename__ = 'table_relation_role'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'))
    privilege_id = db.Column(db.Integer, db.ForeignKey('privileges.id'))

    table = db.relationship('Table', backref='constraint', foreign_keys=[table_id])
    role = db.relationship('Role', backref='constraint', foreign_keys=[role_id])
    privilege = db.relationship('Privilege', backref='constraint', foreign_keys=[privilege_id])

