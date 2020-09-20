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
        self.create_pick_string()
        self.create_game_title()


    def create_pick_string(self):
        if self.pick_type == 'SPREAD':
            if self.pick == self.favorite:
                self.pick_string = self.pick + ' -' + str(self.line)
            else:
                self.pick_string = self.pick + ' +' + str(self.line)
        else:
            self.pick_string = self.pick

    def create_game_title(self):
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
