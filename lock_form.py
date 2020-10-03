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


# def my_length_check(form, field):
#     if len(field.data) > 50:
#         raise ValidationError('Field must be less than 50 characters')

def validate_favorite(form, field):
    if form.favorite.data:
        if (form.favorite.data not in [form.home.data, form.away.data]):
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
        if (form.pick.data not in [form.home.data, form.away.data]):
            raise ValidationError('Pick must match the home or away team')
        elif form.ou.data:
            raise ValidationError("O/U can't have a value for a Spread pick, please switch to Over/Under and clear it out")
        else:
            print("Spread pick validated")

def validate_ou(form, field):
    if form.ou.data:
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

    ou = FloatField('O/U', [Optional()])


    submit = SubmitField('Submit')
