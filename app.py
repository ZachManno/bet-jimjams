from flask import Flask
from flask import render_template, request
from flask_bootstrap import Bootstrap
from flask_simplelogin import SimpleLogin, get_username, login_required

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


class Pick:
    def __init__(self, pick='', home='', away='', favorite='', line=0, ou=0, pick_type='', pick_string='', game_title='', outcome='UNDECIDED'):
        self.pick = pick
        self.home = home
        self.away = away
        self.favorite = favorite
        self.line = line
        self.ou = ou
        self.pick_type = pick_type
        self.outcome = outcome
        if self.pick_type == 'SPREAD':
            if self.pick == self.favorite:
                self.pick_string = self.pick + ' -' + str(self.line)
            else:
                self.pick_string = self.pick + ' +' + str(self.line)
        else:
            self.pick_string = self.pick

        is_favorite_home = self.home == self.favorite
        self.game_title = self.away + ' @ ' + self.home + ' ('
        if is_favorite_home:
            self.game_title += '-' + str(self.line) + ', ' + str(self.ou) + ')'
        else:
            self.game_title += '+' + str(self.line) + ', ' + str(self.ou) + ')'

    @property
    def pick(self):
        return self._pick

    @pick.setter
    def pick(self, value):
        self._pick = value

    @property
    def home(self):
        return self._home

    @home.setter
    def home(self, value):
        self._home = value

    @property
    def away(self):
        return self._away

    @away.setter
    def away(self, value):
        self._away = value

    @property
    def favorite(self):
        return self._favorite

    @favorite.setter
    def favorite(self, value):
        self._favorite = value

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value

    @property
    def ou(self):
        return self._ou

    @ou.setter
    def ou(self, value):
        self._ou = value

    @property
    def pick_type(self):
        return self._pick_type

    @pick_type.setter
    def pick_type(self, value):
        self._pick_type = value

    @property
    def pick_string(self):
        return self._pick_string

    @pick_string.setter
    def pick_string(self, value):
        self._pick_string = value

    @property
    def game_title(self):
        return self._game_title

    @game_title.setter
    def game_title(self, value):
        self._game_title = value

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, value):
        self._outcome = value



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
    p1 = Pick(
        pick="Over",
        home="Eagles",
        away="Rams",
        favorite="Eagles",
        line=1.5,
        ou=57.5,
        pick_type="O/U",
    )
    p2 = Pick(
        pick="Vikings",
        home="Vikings",
        away="Bears",
        favorite="Vikings",
        line=4,
        ou=52.5,
        pick_type="SPREAD",
        outcome="W",
    )
    p3 = Pick(
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

    print("picks list: " + str(picks_list))

    return render_template('home.html', username=get_username().capitalize(), data=picks_list, titles=titles)




