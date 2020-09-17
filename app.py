from flask import Flask
from flask_simplelogin import SimpleLogin
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


secret_key, user_login_dict = load_configs()

print('User login dict: ' + str(user_login_dict))


def only_jimjams_users_login(user):
    """:param user: dict {'username': 'foo', 'password': 'bar'}"""
    username = user.get('username')
    pwd_provided = user.get('password')
    if username in user_login_dict:
        if pwd_provided == user_login_dict[username]:
            return True  # <--- Allowed
    return False  # <--- Denied


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
SimpleLogin(app, login_checker=only_jimjams_users_login)





@app.route('/')
def index():
    return """
    <p style="font-size:xx-large"> <b>Jimjams BET HQ</b> </p>
    """

@app.route('/home')
def home():
    return """
    <p style="font-size:xx-large"> <b>HOME</b> </p>
    """




