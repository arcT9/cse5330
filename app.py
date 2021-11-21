from flask import Flask, render_template, json, request
from model import db_init, User, Role, Privilege, Table, TableConstraint, RoleHasPrivilege
from flask_admin import Admin, expose, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView
import os
import pandas as pd

app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'simplex'
app.secret_key = os.urandom(32)

db = db_init(app)

class UserModelView(ModelView):
    form_columns = ('name', 'phone', 'role')

class RoleModelView(ModelView):
    column_hide_backrefs = False
    column_display_fk = True
    form_columns = ('name', 'description', 'privileges')

class PrivilegeModelView(ModelView):
    form_columns = ('name', 'type')

class TableModelView(ModelView):
    form_columns = ('name', 'owner')

class TableConstraintsView(ModelView):
    column_hide_backrefs = False
    column_exclude_list = None
    form_columns = ('table', 'role', 'privilege')

project = Admin(app, name='CSE 5330 Project 2', template_mode='bootstrap3', url='/db_app', endpoint='proj2', index_view=AdminIndexView(url='/db_app', endpoint='proj2', template='admin/project_2.html'))
project.add_view(UserModelView(User, db.session))
project.add_view(RoleModelView(Role, db.session))
project.add_view(PrivilegeModelView(Privilege, db.session))
project.add_view(TableModelView(Table, db.session))
project.add_view(TableConstraintsView(TableConstraint, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/getUsers')
def get_users():
    data = User.query.all()
    result = [item.format() for item in data]
    return json.dumps(result)

@app.route('/getRoles')
def get_roles():
    data = Role.query.all()
    result = [item.format() for item in data]
    return json.dumps(result)

@app.route('/getPrivileges')
def get_privileges():
    data = Privilege.query.all()
    result = [item.format() for item in data]
    return json.dumps(result)

@app.route('/checkPrivilege/<int:user_id>')
def check_privilege(user_id):
    privileges = pd.read_sql(f'''
        SELECT p.name as p_name, r.name as r_name, u.name as u_name FROM privileges AS p
        JOIN role_has_privilege AS rhp ON rhp.privilege_id=p.id
        JOIN roles AS r ON r.id=rhp.role_id
        JOIN user AS u ON u.role_id=r.id
        WHERE u.id={user_id}
    ''', con=db.session.connection())
    result = {
        'user': privileges['u_name'].tolist()[0],
        'role': privileges['r_name'].tolist()[0],
        'privileges': privileges['p_name'].tolist()
    }
    if result.get('role')=='db_owner':
        table = pd.read_sql(f'''
        SELECT name from tables where owner_id={user_id}
        ''', con=db.session.connection())
        result['owns']=table['name'].tolist()
    return json.dumps(result)

@app.route('/checkRolePrivilege/<int:role_id>')
def check_role_privilege(role_id):
    privileges = pd.read_sql(f'''
        SELECT p.name as p_name, r.name as r_name FROM privileges AS p
        JOIN role_has_privilege AS rhp ON rhp.privilege_id=p.id
        JOIN roles AS r ON r.id=rhp.role_id
        WHERE r.id={role_id}
    ''', con=db.session.connection())
    users = pd.read_sql(f'''
        SELECT name from user
        WHERE role_id={role_id}
    ''', con=db.session.connection())
    result = {}
    if not privileges.empty:
        result['privileges'] = privileges.get('p_name').tolist(),
        result['role'] = privileges.get('r_name').tolist()[0]
    else: 
        result['privileges'] = None,
        result['role'] = None
    if not users.empty:
        result['users'] = users.get('name').tolist()
    else:
        result['users'] = None
    return json.dumps(result)

@app.route('/checkUserPrivilege/<int:user_id>/<int:privilege_id>')
def check_user_privilege(user_id, privilege_id):
    privileges = pd.read_sql(f'''
        SELECT p.id FROM privileges AS p
        JOIN role_has_privilege AS rhp ON rhp.privilege_id=p.id
        JOIN roles AS r ON r.id=rhp.role_id
        JOIN user AS u ON u.role_id=r.id
        WHERE u.id={user_id}
    ''', con=db.session.connection())['id'].tolist()
    return json.dumps('yes' if int(privilege_id) in privileges else 'no')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=env.get('PORT', 3000))
