from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 6)])
    submit = SubmitField("Login")
    
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min = 3)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 6)])
    submit = SubmitField("Register")
    
#Code ends here