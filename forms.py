from flask_wtf import FlaskForm
from typing import Sized

from wtforms import TextField, PasswordField, StringField, SelectField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired,DataRequired, EqualTo, Length
from wtforms.widgets.core import TextArea

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
    phonenumber = StringField(
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
    submit = SubmitField('Registrar')

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
    phonenumber = StringField(
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
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    usr = StringField('Usuario *',validators=[DataRequired(message='Se requiere el usuario'), Length(min=6, max=40, message='Longitud debe estar entre 6 y 40')])
    pwd = PasswordField('Contraseña *',validators=[DataRequired(message='Se requiere la clave')])
    btn = SubmitField('Login')


class ForgotForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

# Clase del formulario Dashboard - medico
class DashBoardMedico(FlaskForm):
    tipoid = SelectField(u'Tipo de identificación ', choices=[('C.C'), ('T.I'), ('T.E')])
    id = StringField('No. ID', validators = [DataRequired(message='Se requiere el ID')])
    name = StringField('Nombres', validators = [DataRequired(message='Se requiere el nombre')])
    last = StringField('Apellidos', validators = [DataRequired(message='Se requiere el apellido'), Length(min=2, max=40)])
    especialidad = SelectField(u'Especialidad ', choices=[('General'), ('Odontología'), ('Pediatría')])
    phone = StringField('Telefono', validators = [DataRequired(message='Se requiere el teléfono'), Length(min=2, max=40)])
    time = SelectField(u'Hora de atención', choices=[('9:00'), ('12:30'), ('16:00')])
    user = StringField('Usuario', validators = [DataRequired(message='Se requiere nombre de usuario'), Length(min=2, max=40)])
    password = PasswordField('Contraseña', [DataRequired(message='Se requiere la clave')])
    email = TextField('Correo electrónico', validators = [DataRequired(message='Se requiere el correo electrónico'), Length(min=2, max=40)])

#Clase del formulario crear cita
class CitaForm(FlaskForm):
    tipoid = SelectField(u'Tipo de identificación ', choices=[('C.C'), ('T.I'), ('T.E')])
    id = TextField('No. ID', validators = [DataRequired(message='Se requiere el ID')])
    medico = SelectField(u'Medico ', choices=[('Daniel R.'), ('Lorena P.'), ('Katiana A.')])
    especialidad = SelectField(u'Especialidad ', choices=[('General'), ('Odontología'), ('Pediatría')])
    time = SelectField(u'Hora de atención', choices=[('9:00'), ('12:30'), ('16:00')])
    paciente = TextField('Nombre', validators = [DataRequired(message='Se requiere nombre del paciente'), Length(min=2, max=40)])
    apellido = TextField('Apellido', validators = [DataRequired(message='Se requiere apellido del paciente'), Length(min=2, max=40)])
    id_paciente = TextField('No ID', [DataRequired(message='Se requiere la clave')])
    email = TextField('Correo electrónico', validators = [DataRequired(message='Se requiere el correo electrónico'), Length(min=2, max=40)])
    comentario = TextAreaField("TextArea")
    fecha = DateField('Fecha', validators = [DataRequired(message='Se requiere la fecha')])

# Clase del formulario dashboard paciente

class Paciente(FlaskForm):
   selTipId   = SelectField(u'Tipo de Identificación', choices=[('cc', 'Cedula'), ('pp', 'Pasaporte'), ('ti', 'Tarjeta Identidad')])
   txtNroDoc  = TextField('Nro. documento*',validators=[InputRequired(message='Digite el Nro de documento')])
   TxtNombres = TextField('Nombres*', validators=[InputRequired(message='Digite el nombre(s)')])
   TxtApellidos = TextField(' Apellidos *', validators=[InputRequired(message='Digite los apellidos')])
   TxtNroCel = TextField(' Nro Celular *', validators=[InputRequired(message='Digite nro Celular')])
   DateFecha = DateField('Fecha de Nacimiento',format='%Y-%m-%d')
   selSexo =  SelectField(u'Genero', choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]) 
   selGrupoRh = SelectField(u'Grupo Sanguineo', choices=[('A+', 'A+'), ('A-', 'A-'), ('O+', 'O+')]) 
   txtUsuario = TextField('Usuario *', validators=[InputRequired(message='Ingrese Usuario')])
   PwdClave = PasswordField('Contraseña *',validators=[InputRequired(message='Se requiere la clave')])    
   mailUsuario = EmailField('Email *', validators=[InputRequired(message='Digite el correo electrónico')])
   btnReg = SubmitField('Registrar') 
   btnEditar = SubmitField('Editar')
   btnEliminar = SubmitField('Eliminar')
   btnNotificar = SubmitField('Notificar')
   btnSalir = SubmitField('Salir')

# Clase del formulario dashboard Cita
class Cita(FlaskForm):
   txtNroCita = TextField('Nro. Cita*',validators=[InputRequired(message='Digite el Nro de cita')])
   selEspecialidad   = SelectField(u'Especialidad', choices=[('01', 'Cardiologo'), ('02', 'Ortopedista'), ('03', 'Hemologo')])
   selMedico   = SelectField(u'Medico', choices=[('01', 'Carlos Arturo'), ('02', 'Pedro Gonzalez'), ('03', 'Juan Mejia')])
   DateFecha = DateField('Fecha ',format='%Y-%m-%d')
   selhora   = SelectField(u'Hora', choices=[('08', '8:a.m'), ('09', '9:a.m'), ('10', '10:a.m')])
   tipoid = SelectField(u'Tipo de identificación ', choices= [('cc', 'Cedula'), ('pp', 'Pasaporte'), ('ti', 'Tarjeta Identidad')])
   txtNroDoc  = TextField('Nro. documento*',validators=[InputRequired(message='Digite el Nro de documento')])
   TxtNombres = TextField('Nombres*', validators=[InputRequired(message='Digite el nombre(s)')])
   TxtApellidos = TextField(' Apellidos *', validators=[InputRequired(message='Digite los apellidos')])
   mailUsuario = EmailField('Email *', validators=[InputRequired(message='Digite el correo electrónico')])
   Comentarios = TextAreaField('Comentarios')
   btnReg = SubmitField('Reservar') 
   btnEditar = SubmitField('Editar')
   btnEliminar = SubmitField('Eliminar')
   btnNotificar = SubmitField('Notificar')
   btnSalir = SubmitField('Salir')

class Perfil(FlaskForm):
    usr = StringField('Usuario *',validators=[DataRequired(message='Se requiere el usuario'), Length(min=6, max=40, message='Longitud debe estar entre 6 y 40')])
    pwd = PasswordField('Contraseña *',validators=[DataRequired(message='Se requiere la clave')])
    mailUsuario = EmailField('Email *', validators=[InputRequired(message='Digite el correo electrónico')])

class VistaBusquedas(FlaskForm):
    usr = StringField('Usuario *',validators=[DataRequired(message='Se requiere el usuario'), Length(min=6, max=40, message='Longitud debe estar entre 6 y 40')])

