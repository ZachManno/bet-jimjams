from flask import Flask
from flask import render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_simplelogin import SimpleLogin, get_username, login_required

import pick
import dynamo
import lock_form

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
    username = get_username()
    titles = [('pick_string', 'Pick'), ('outcome', 'Outcome'), ('game_title', 'Game'), ('pick_type', 'Pick Type')]

    weeks_available = dynamo.get_weeks_available(username)
    picks_for_each_week = []
    for week in weeks_available:
        picks_for_each_week.append(
                                   (str(week), dynamo.get_picks_for_user_for_week(username, week)))


    print("Picks for each week: " + str(picks_for_each_week))
    return render_template('home.html', username=username.capitalize(), picks_for_each_week=picks_for_each_week, titles=titles, header_classes='text-info', table_classes="table-striped table-bordered table-sm")


@app.route('/lock-form/', methods=('GET', 'POST'))
def lock_form_route():
    form = lock_form.LockForm()
    if form.validate_on_submit():
        username = get_username()
        print("Form for week " + str(form.week.data) + " validated")
        p = lock_form.convert_form_to_pick_obj(form)
        print("Pick obj: " + str(p.__dict__))
        dynamo.insert_pick(username, p)
        return redirect('/en')
    else:
        print("Not validated")
    return render_template('add-lock.html', form=form)



# resolve?home=Cowboys&away=Vikings&type=spread&result=w
@app.route('/resolve')
def landing_page():
    username = get_username()
    home = request.args['home']
    away = request.args['away']
    pick_type = request.args['type']
    result = request.args['result'].upper()
    print("home: " + home)
    print("pick_type: " + pick_type)
    return render_template('index.html')




