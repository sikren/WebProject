from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    email = StringField('email')
    about = StringField('about')

    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired()])

    submit = SubmitField('Submit', validators=[DataRequired()])
