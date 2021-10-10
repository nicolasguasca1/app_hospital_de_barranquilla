from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, SelectField
from wtforms import validators
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
    sex = SelectField('state', choices=['-','Masculino','Femenino'])
    rh = SelectField('state', choices=['-','O-','O+','A-','A+','B-','B+','AB-','AB+',])
    phonenumber = TextField(
        'Número de teléfono', validators=[DataRequired(), Length(min=6, max=25)]
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
    sex = SelectField('state', choices=['-','Masculino','Femenino'])
    rh = SelectField('state', choices=['-','O-','O+','A-','A+','B-','B+','AB-','AB+',])
    phonenumber = TextField(
        'Número de teléfono', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'Correo electrónico', validators=[DataRequired(), Length(min=6, max=40)]
    )
    professionalId = StringField(
        'Número de tarjeta profesional', validators=[DataRequired(), Length(min=6, max=40)]
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


class LoginForm(FlaskForm):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(FlaskForm):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

# Clase del formulario Dashboard - medico
class MedicForm(FlaskForm):
    tipoid = SelectField(u'Tipo de identificación ', choices=[('C.C'), ('T.I'), ('T.E')])
    id = TextField('No. ID', validators = [DataRequired()])
    name = TextField('Nombres', validators = [DataRequired()])
    last = TextField('Apellidos', validators = [DataRequired(), Length(min=2, max=40)])
    especialidad = SelectField(u'Especialidad ', choices=[('General'), ('Odontología'), ('Pediatría')])
    phone = TextField('Telefono', validators = [DataRequired(), Length(min=2, max=40)])
    time = SelectField(u'Hora de atención', choices=[('9:00'), ('12:30'), ('16:00')])
    user = TextField('Usuario', validators = [DataRequired(), Length(min=2, max=40)])
    password = PasswordField('Contraseña', [DataRequired()])
    email = TextField('Correo electrónico', validators = [DataRequired(), Length(min=2, max=40)])
