from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Email, Length, EqualTo


class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 16) ])
    submit = SubmitField("sumbit")

class Sigup(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(8,)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 16) ])
    # password_confirmation = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("Password")])
    submit = SubmitField("sumbit")