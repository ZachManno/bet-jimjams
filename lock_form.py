from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField,
                     TextField,
                     FloatField,
                     BooleanField,
                     IntegerField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL,ValidationError, Optional)

import pick

def validate_favorite(form, field):
    if form.favorite.data:
        if (form.favorite.data.upper() not in [form.home.data.upper(), form.away.data.upper()]):
            raise ValidationError('Favorite must match the home or away team')
        elif form.ou.data:
            raise ValidationError("O/U can't have a value for a Spread pick, please switch to Over/Under and clear it out")
        else:
            print("favorite validated")

def validate_pick(form, field):
    if form.ou.data:
        if form.pick.data.upper() not in ['OVER', 'UNDER']:
            raise ValidationError("Over under pick must be OVER or UNDER")
    else:
        if (form.pick.data.upper() not in [form.home.data.upper(), form.away.data.upper()]):
            raise ValidationError('Pick must match the home or away team')
        elif form.ou.data:
            raise ValidationError("O/U can't have a value for a Spread pick, please switch to Over/Under and clear it out")
        else:
            print("Spread pick validated")

def validate_ou(form, field):
    if form.ou.data:
        print("form.ou.data: " + str(form.ou.data))
        if form.line.data:
            raise ValidationError("Line can't have a value for an Over/Under pick, please switch to Spread and clear it out")
        if form.favorite.data:
            raise ValidationError("Favorite can't have a value for an Over/Under pick, please switch to Spread and clear it out")
        if float(form.ou.data) < 30:
            raise ValidationError("Ehhh are you sure the O/U is that low??")
        if float(form.ou.data) > 70:
            raise ValidationError("Ehh are you sure the O/U is that high??")
    print("ou validated")



class LockForm(FlaskForm):
    """Lock form."""
    week = IntegerField('Week', [
        DataRequired()
        ])
    home = StringField('Home', [
        DataRequired()
        ])
    away = StringField('Away', [
        DataRequired()
        ])
    favorite = StringField('Favorite', [validate_favorite])
    pick = StringField('Pick', [validate_pick])
    line = FloatField('Line', [Optional()])

    ou = FloatField('O/U', [Optional(), validate_ou])

    submit = SubmitField('Submit')


def convert_form_to_pick_obj(form):
    if form.ou.data:
        return pick.Pick(pick=form.pick.data.upper(), home=form.home.data.lower().capitalize(), away=form.away.data.lower().capitalize(), ou=form.ou.data, week=form.week.data, pick_type='O/U')
    else:
        return pick.Pick(pick=form.pick.data.lower().capitalize(), home=form.home.data.lower().capitalize(), away=form.away.data.lower().capitalize(), favorite=form.favorite.data, line=form.line.data, week=form.week.data, pick_type='SPREAD')





