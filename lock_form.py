from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField,
                     TextField,
                     FloatField,
                     BooleanField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL,ValidationError, Optional)


# def my_length_check(form, field):
#     if len(field.data) > 50:
#         raise ValidationError('Field must be less than 50 characters')

def validate_favorite(form, field):
    if (form.favorite.data not in [form.home.data, form.away.data]):
        raise ValidationError('Favorite must match the home or away team')
    else:
        print("validated")

class LockForm(FlaskForm):
    """Lock form."""
    home = StringField('Home', [
        DataRequired()
        ])
    away = StringField('Away', [
        DataRequired()
        ])
    favorite = StringField('Favorite', [
        DataRequired(), validate_favorite])
    pick = StringField('Pick', [
        #DataRequired()
        ])
    line = FloatField('Line', [
        #DataRequired()
        ])

    ou = FloatField('O/U', [Optional()])


    submit = SubmitField('Submit')
