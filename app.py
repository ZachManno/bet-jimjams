from flask import Flask
from flask import render_template, request
from flask_bootstrap import Bootstrap
from flask_simplelogin import SimpleLogin, get_username, login_required

from flask_sqlalchemy import SQLAlchemy

import os


def load_configs():
    users_list = ['DANNY_LOGIN_USER_PWD', 'HEINS_LOGIN_USER_PWD', 'PAT_LOGIN_USER_PWD', 'MANNO_LOGIN_USER_PWD']
    login_dict = dict()
    for user in users_list:
        userpwd_combo = os.environ.get(user).split('-')
        username = userpwd_combo[0]
        pwd = userpwd_combo[1]
        login_dict[username] = pwd

    secret_key = os.environ.get('LOGIN_SECRET_KEY')
    return secret_key, login_dict


def only_jimjams_users_login(user):
    """:param user: dict {'username': 'foo', 'password': 'bar'}"""
    username = user.get('username')
    pwd_provided = user.get('password')
    if username in user_login_dict:
        if pwd_provided == user_login_dict[username]:
            return True  # <--- Allowed
    return False  # <--- Denied



secret_key, user_login_dict = load_configs()
#print('User login dict: ' + str(user_login_dict))

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SIMPLELOGIN_HOME_URL'] = '/en/'
SimpleLogin(app, login_checker=only_jimjams_users_login)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

class Pick:
    def __init__(self, team="", line='', pick_type=""):
        self.team = team
        self.line = line
        self.pick_type = pick_type
    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, value):
        self._team = value

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value

    @property
    def pick_type(self):
        return self._pick_type

    @pick_type.setter
    def pick_type(self, value):
        self._pick_type = value

db.create_all()
for i in range(20):
        m = Message(
            text='Test message {}'.format(i+1),
            )
        db.session.add(m)

db.session.commit()



# ---------------------------------------------
# ---------- Routes Start ---------------------
# ---------------------------------------------
# ---------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/en/')
def home():
    print('at home')
    data1 = {"pick1": "Vikings"}
    data2 = {"pick2": "Cowboys"}
    data_list = []
    data_list.append(data1)
    data_list.append(data2)


    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page, per_page=10)
    messages = pagination.items

    #titles = [('index', '#'), ('text', 'Pick')]
    titles = [('team', 'Team'), ('line', 'Line'), ('pick_type', 'Pick Type')]

    print("messages: " + str(messages))
    print("type messages: " + str(type(messages)))




    picks_list = []
    p1 = Pick(
        team="Over",
        line="56.5",
        pick_type="O/U",
    )
    p2 = Pick(
        team="Vikings",
        line="-3",
        pick_type="SPREAD",
    )
    p3 = Pick(
        team="Cowboys",
        line="+4.5",
        pick_type="SPREAD",
    )
    picks_list.append(p1)
    picks_list.append(p2)
    picks_list.append(p3)

    print("picks list: " + str(picks_list))

    return render_template('home.html', username=get_username().capitalize(), data=picks_list, titles=titles)




