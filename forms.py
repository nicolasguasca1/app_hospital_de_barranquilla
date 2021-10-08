from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterFormPac(FlaskForm):
    name = StringField(
        'Nombres', validators=[DataRequired(), Length(min=6, max=25)]
    )
    lastname = StringField(
        'Apellidos', validators=[DataRequired(), Length(min=6, max=25)]
    )
    id = StringField(
        'Número de identificación', validators=[DataRequired(), Length(min=6, max=25)]
    )
    birthdate = DateField(
        'Fecha de nacimiento', format='%d-%m-%Y' 
    )
    email = StringField(
        'Correo electrónico', validators=[DataRequired(), Length(min=6, max=40)]
    )
    username = StringField(
        'Defina un nombre de usuario', validators=[DataRequired(), Length(min=6, max=25)]
    )
    password = PasswordField(
        'Defina una contraseña', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repetir contraseña',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )

class RegisterFormMed(FlaskForm):
    name = TextField(
        'nombre', validators=[DataRequired(), Length(min=6, max=25)]
    )
    lastname = TextField(
        'apellido', validators=[DataRequired(), Length(min=6, max=25)]
    )
    id = TextField(
        'número de identificación', validators=[DataRequired(), Length(min=6, max=25)]
    )
    birthdate = TextField(
        'fecha de nacimiento', validators=[DataRequired(), Length(min=6, max=25)]
    )
    username = TextField(
        'nombre de usuario', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Correo electrónico', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Contraseña', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repetir contraseña',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(FlaskForm):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(FlaskForm):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
