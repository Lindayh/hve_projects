from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

class LoginForm(FlaskForm):
    username = StringField('username', [InputRequired(), Length(min=1)], render_kw={"placeholder":"Enter username"})
    password = PasswordField(validators=[InputRequired(), Length(min=1)], render_kw={"placeholder":"Enter password"})
    submit = SubmitField('Login')

    # def validate_username(self, username):  #18:05
    #     pass