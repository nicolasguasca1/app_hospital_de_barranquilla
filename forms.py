from flask_wtf import FlaskForm
from typing import Sized

from wtforms import TextField, PasswordField, StringField, SelectField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length
from wtforms.widgets.core import TextArea
from db import seleccion

# Set your classes here.


class RegisterFormPac(FlaskForm):
    name = StringField(
        'Nombres *', validators=[DataRequired(), Length(min=6, max=25)]
    )
    lastname = StringField(
        'Apellidos *', validators=[DataRequired(), Length(min=6, max=25)]
    )
    tipoid = SelectField(u'Tipo de identificación ', choices=[(
        'Cédula de ciudadanía'), ('Pasaporte'), ('Tarjeta de identidad'), ('Cédula de extranjería')])
    id = StringField(
        'Número de identificación', validators=[DataRequired(), Length(min=6, max=25)]
    )
    birthdate = DateField(
        'Fecha de nacimiento', format='%d-%m-%Y'
    )
    sex = SelectField('state', choices=['-', 'Masculino', 'Femenino'])
    rh = SelectField('state', choices=[
                     '-', 'O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+', ])
    phonenumber = StringField(
        'Número de teléfono', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'micorreo@ejemplo.com', validators=[DataRequired(), Length(min=6, max=40)]
    )
    username = StringField(
        'miusuarioejemplo', validators=[DataRequired(), Length(min=6, max=25)]
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
    tipoid = SelectField(u'Tipo de identificación ', choices=[(
        'Cédula de ciudadanía'), ('Pasaporte'), ('Tarjeta de identidad'), ('Cédula de extranjería')])
    specialty = SelectField(u'Especialidad', choices=[(
        'Cardiología'), ('Podología'), ('Dermatología'), ('Psiquiatría'), ('Medicina Interna'), ('Medicina familiar'), ('Pediatría'), ('Geriatría'), ('Urología'), ('Oncología'), ('Hematología'), ('Ginecología y obstetricia'), ('Gastroenterología'), ('Medicina laboral'), ('Endocrinología'), ('Neurocirugía')])
    birthdate = DateField(
        'Fecha de nacimiento', format='%d-%m-%Y'
    )
    sex = SelectField('state', choices=['-', 'Masculino', 'Femenino'])
    rh = SelectField('state', choices=[
                     '-', 'O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+', ])
    modalidad = SelectField('state', choices=['MAÑANA', 'TARDE'])
    phonenumber = StringField(
        'Número de teléfono', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'Correo electrónico', validators=[DataRequired(), Length(min=6, max=40)]
    )
    professionalId = StringField(
        'Número de médico registrado para ejercer', validators=[DataRequired(), Length(min=6, max=40)]
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
    usr = StringField('Usuario *', validators=[DataRequired(message='Se requiere el usuario'), Length(
        min=6, max=40, message='Longitud debe estar entre 6 y 40')])
    pwd = PasswordField(
        'Contraseña *', validators=[DataRequired(message='Se requiere la clave')])
    btn = SubmitField('Login')


class ForgotForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

# Clase del formulario Dashboard - medico


class DashBoardMedico(FlaskForm):
    sqlesp = f"SELECT especialidad FROM Especialidades"
    sqltipoid = f"SELECT Tipo FROM TipoId"
    sqlmod = f"SELECT modalidad FROM Modalidades"
    resmod = seleccion(sqlmod)
    restipoid = seleccion(sqltipoid)
    resesp = seleccion(sqlesp)
    dataEsp = []
    datamod = []
    dataTipoId = []
    i = 0
    while i < len(resmod):
        datamod.append(resmod[i][0])
        i += 1
    i = 0
    while i < len(restipoid):
        dataTipoId.append(restipoid[i][0])
        i += 1
    i = 0
    while i < len(resesp):
        dataEsp.append(resesp[i][0])
        i += 1

    tipoid = SelectField(u'Tipo de identificación ',
                         choices=dataTipoId)
    id = StringField('No. ID', validators=[
                     DataRequired(message='Se requiere el ID')])
    name = StringField('Nombres', validators=[
                       DataRequired(message='Se requiere el nombre')])
    last = StringField('Apellidos', validators=[DataRequired(
        message='Se requiere el apellido'), Length(min=2, max=40)])
    especialidad = SelectField(u'Especialidad actual: ', choices=dataEsp)
    phone = StringField('Telefono')
    time = SelectField(u'Jornada de trabajo actual: ', choices=datamod)
    user = StringField('Usuario', validators=[DataRequired(
        message='Se requiere nombre de usuario'), Length(min=2, max=40)])
    password = PasswordField('Contraseña')
    email = TextField('Correo electrónico', validators=[DataRequired(
        message='Se requiere el correo electrónico'), Length(min=2, max=40)])
    CreateRegMed = SubmitField('Crear Registro')
    UpdateRegMed = SubmitField('Actualizar')
    DeleteRegMed = SubmitField('Eliminar')
    SearchRegMed = SubmitField('Buscar')
    RecoveryRegMed = SubmitField('Recuperar')

# Clase del formulario crear cita


class CitaForm(FlaskForm):
    # Preparar consulta
    # traer especialidades de la DB
    sqlesp = f"SELECT especialidad FROM Especialidades"

    # traer id de pacientes
    resesp = seleccion(sqlesp)

    dataEsp = []
    i = 0
    while i < len(resesp):
        dataEsp.append(resesp[i][0])
        i += 1

    medico = SelectField(u'Medico')
    idm = TextField('ID Médico', validators=[DataRequired(
        message='Se requiere ID'), Length(min=2, max=40)])
    especialidad = SelectField(u'Especialidad', choices=dataEsp)
    time = SelectField(u'Hora de atención')
    paciente = TextField('Nombre', validators=[DataRequired(
        message='Se requiere el nombre'), Length(min=2, max=40)])
    apellido = TextField('Apellido', validators=[DataRequired(
        message='Se requiere apellido del paciente'), Length(min=2, max=40)])
    tipoid = TextField('Tipo de ID', validators=[DataRequired(
        message='Se requiere el id'), Length(min=2, max=40)])
    id_paciente = TextField('ID Paciente', validators=[DataRequired(
        message='Se requiere el id'), Length(min=2, max=40)])
    email = TextField('Correo electrónico', validators=[DataRequired(
        message='Se requiere el correo electrónico'), Length(min=2, max=40)])
    fecha = DateField('Fecha', validators=[
                      DataRequired(message='Se requiere la fecha')])

# Clase del formulario dashboard paciente


class DashBoardPaciente(FlaskForm):

    #sqlgrh = f"SELECT descripcion FROM Grupo Sanguineo"
    sqltipoid = f"SELECT Tipo FROM TipoId"
    sqlsex = f"SELECT descripcion FROM Sexo"
    #resgrh = seleccion(sqlgrh)
    restipoid = seleccion(sqltipoid)
    ressex = seleccion(sqlsex)
    #datagrh = []
    datasex = []
    dataTipoId = []
    #i = 0
    # while i < len(resgrh):
    #    datagrh.append(resgrh[i][0])
    #    i += 1
    i = 0
    while i < len(restipoid):
        dataTipoId.append(restipoid[i][0])
        i += 1
    i = 0
    while i < len(ressex):
        datasex.append(ressex[i][0])
        i += 1

    selTipId = SelectField(u'Tipo de Identificación', choices=dataTipoId)

    txtNroDoc = TextField(
        'Nro. documento*', validators=[InputRequired(message='Digite el Nro de documento')])
    TxtNombres = TextField(
        'Nombres*', validators=[InputRequired(message='Digite el nombre(s)')])
    TxtApellidos = TextField(
        ' Apellidos *', validators=[InputRequired(message='Digite los apellidos')])
    TxtNroCel = TextField(
        ' Nro Celular *', validators=[InputRequired(message='Digite nro Celular')])
    DateFecha = DateField('Fecha de Nacimiento', format='%Y-%m-%d')
    selSexo = SelectField(u'Genero: ', choices=datasex)
    selGrupoRh = SelectField(u'Grupo Sanguineo: ', choices=[
                             ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    txtUsuario = TextField(
        'Usuario *', validators=[InputRequired(message='Ingrese Usuario')])
    PwdClave = PasswordField(
        'Contraseña *')
    mailUsuario = EmailField(
        'Email *', validators=[InputRequired(message='Digite el correo electrónico')])

    CreateRegPac = SubmitField('Crear Registro')
    UpdateRegPac = SubmitField('Actualizar')
    DeleteRegPac = SubmitField('Eliminar')
    SearchRegPac = SubmitField('Buscar')
    RecoveryRegPac = SubmitField('Recuperar')


# Clase del formulario dashboard Cita


class Cita(FlaskForm):
    txtNroCita = TextField(
        'Nro. Cita*', validators=[InputRequired(message='Digite el Nro de cita')])
    selEspecialidad = SelectField(u'Especialidad', choices=[(
        '01', 'Cardiologo'), ('02', 'Ortopedista'), ('03', 'Hemologo')])
    selMedico = SelectField(u'Medico', choices=[(
        '01', 'Carlos Arturo'), ('02', 'Pedro Gonzalez'), ('03', 'Juan Mejia')])
    DateFecha = DateField('Fecha ', format='%Y-%m-%d')
    selhora = SelectField(
        u'Hora', choices=[('08', '8:a.m'), ('09', '9:a.m'), ('10', '10:a.m')])
    tipoid = SelectField(u'Tipo de identificación ', choices=[
                         ('cc', 'Cedula'), ('pp', 'Pasaporte'), ('ti', 'Tarjeta Identidad')])
    txtNroDoc = TextField(
        'Nro. documento*', validators=[InputRequired(message='Digite el Nro de documento')])
    TxtNombres = TextField(
        'Nombres*', validators=[InputRequired(message='Digite el nombre(s)')])
    TxtApellidos = TextField(
        ' Apellidos *', validators=[InputRequired(message='Digite los apellidos')])
    mailUsuario = EmailField(
        'Email *', validators=[InputRequired(message='Digite el correo electrónico')])
    Comentarios = TextAreaField('Comentarios')

    btnReg = SubmitField('Reservar')
    btnEditar = SubmitField('Editar')
    btnEliminar = SubmitField('Eliminar')
    btnNotificar = SubmitField('Notificar')
    btnSalir = SubmitField('Salir')


class Perfil(FlaskForm):
    usr = StringField('Usuario *', validators=[Length(
        min=6, max=40, message='Longitud debe estar entre 6 y 40')])
    pwd = PasswordField(
        'Contraseña *')
    confirm = PasswordField(
        'Contraseña *')
    mailUsuario = EmailField(
        'Email *')
    usrUpdate = SubmitField('Actualizar usuario')
    pwdUpdate = SubmitField('Actualizar contraseña')
    mailUsuarioUpdate = SubmitField('Actualizar correo electrónico')


class VistaBusquedas(FlaskForm):
    usr = StringField('Usuario *', validators=[DataRequired(message='Se requiere el usuario'), Length(
        min=6, max=40, message='Longitud debe estar entre 6 y 40')])
