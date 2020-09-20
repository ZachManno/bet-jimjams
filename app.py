from flask import Flask
from flask import render_template, request
from flask_bootstrap import Bootstrap
from flask_simplelogin import SimpleLogin, get_username, login_required

import pick

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


# ---------------------------------------------
# ---------- Routes Start ---------------------
# ---------------------------------------------
# ---------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/en/')
def home():
    titles = [('game_title', 'Game'), ('pick_string', 'Pick'), ('pick_type', 'Pick Type'), ('outcome', 'Outcome')]


    picks_list = []
    p1 = pick.Pick(
        pick="Over",
        home="Eagles",
        away="Rams",
        favorite="Eagles",
        line=1.5,
        ou=57.5,
        pick_type="O/U",
    )
    p2 = pick.Pick(
        pick="Vikings",
        home="Vikings",
        away="Bears",
        favorite="Vikings",
        line=4,
        ou=52.5,
        pick_type="SPREAD",
        outcome="W",
    )
    p3 = pick.Pick(
        pick="Giants",
        home="Cardinals",
        away="Giants",
        favorite="Cardinals",
        line=6,
        ou=48,
        pick_type="SPREAD",
        outcome="L",
    )

    picks_list.append(p1)
    picks_list.append(p2)
    picks_list.append(p3)

    return render_template('home.html', username=get_username().capitalize(), data=picks_list, titles=titles, table_classes="table-striped table-bordered")




