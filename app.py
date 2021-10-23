#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from markupsafe import escape
import os
from flask_user import current_user, login_required, roles_required, UserManager
from flask_login import LoginManager, login_user, UserMixin
# from models import get_user, users, User
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
from utils import login_valido, pass_valido, email_valido
from db import accion, seleccion


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
# login_manager = LoginManager(app)
# login_manager.login_view = "login"
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login manager decorator.
# @login_manager.user_loader
# def load_user(user_id):
#     for user in users:
#         if user.id == int(user_id):
#             return user
#     return None

# Login required function

'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
@app.route('/home/', methods=['GET'])
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/privacy')
def privacy():
    return render_template('pages/placeholder.privacy.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if session['usr_id']:
    #     return redirect(url_for('home'))
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('forms/login.html', form=form)
    else:
        # Recuperar los datos
        usr = escape(form.usr.data.strip())
        pwd = escape(form.pwd.data.strip())
        # Validar los datos
        swvalido = True
        if len(usr) < 6 or len(usr) > 40:
            swvalido = False
            flash("El nombre de usuario es requerido y tiene entre 6 y 40 caracteres")
        if len(pwd) < 6 or len(pwd) > 40:
            swvalido = False
            flash("El nombre de usuario es requerido y tiene entre 6 y 40 caracteres")
        # Preparar la consulta
        sqlmed = f"SELECT idmedico, nombres, mail, clave, idrol FROM Médico WHERE usuario = '{usr}'"
        sqlpac = f"SELECT idpaciente, nombres, mail, clave, idrol FROM Paciente WHERE usuario = '{usr}'"
        sqladmin = f"SELECT idsuper, nombres, mail, clave, idrol FROM Superusuario WHERE usuario = '{usr}'"

        # Ejecutar la consulta
        resmed = seleccion(sqlmed)
        respac = seleccion(sqlpac)
        resadmin = seleccion(sqladmin)
        # Proceso los resultados
        if len(resmed) != 0:
            cbd = resmed[0][3]  # Recuperar la clave
            if check_password_hash(cbd, pwd):
                session.clear()
                session['id'] = resmed[0][0]
                session['nom'] = resmed[0][1]
                session['usr'] = usr
                session['cla'] = pwd
                session['ema'] = resmed[0][2]
                session['rol'] = resmed[0][4]
                return render_template('pages/placeholder.home.html')
            else:
                flash('ERROR: Usuario o clave invalidos1')
                return render_template('forms/login.html', form=form)
        elif len(respac) != 0:
            cbd = respac[0][3]  # Recuperar la clave
            if check_password_hash(cbd, pwd):
                session.clear()
                session['id'] = respac[0][0]
                session['nom'] = respac[0][1]
                session['usr'] = usr
                session['cla'] = pwd
                session['ema'] = respac[0][2]
                session['rol'] = respac[0][4]
                return render_template('pages/placeholder.home.html')
            else:
                flash('ERROR: Usuario o clave invalidos2')
                return render_template('forms/login.html', form=form)
        elif len(resadmin) != 0:
            cbd = resadmin[0][3]  # Recuperar la clave
            if check_password_hash(cbd, pwd):
                session.clear()
                session['id'] = resadmin[0][0]
                session['nom'] = resadmin[0][1]
                session['usr'] = usr
                session['cla'] = pwd
                session['ema'] = resadmin[0][2]
                session['rol'] = resadmin[0][4]
                return render_template('pages/placeholder.home.html')
            else:
                flash('ERROR: Usuario o clave invalidos3')
                return render_template('forms/login.html', form=form)

        # elif form.btn():
        #     login_user(user)
        #     flash('Ha iniciado sesión correctamente.')
        else:
            flash('ERROR: Usuario o clave invalidos4')
            return render_template('forms/login.html', form=form)


@app.route('/registropac', methods=['GET', 'POST'])
def registropac():
    pacform = RegisterFormPac(request.form)

    if request.method == 'GET':
        return render_template('forms/registropac.html', form=pacform)
    else:
        # Recuperar los datos del formulario
        name = escape(request.form['name'])
        lastname = escape(request.form['lastname'])
        tipoid = escape(request.form['tipoid'])
        id = escape(request.form['id'])
        birthdate = escape(request.form['birthdate'])
        sex = escape(request.form['sex'])
        rh = escape(request.form['rh'])
        phonenumber = escape(request.form['phonenumber'])
        email = escape(request.form['email'])
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        confirm = escape(request.form['confirm'])
        role = 1
        # Validar los datos
        swerror = False
        if id == None or len(id) == 0:
            flash('ERROR: Debe suministrar un numero de identificación')
            swerror = True
        if username == None or len(username) == 0 or not login_valido(username):
            flash('ERROR: Debe suministrar un usuario válido ')
            swerror = True
        if email == None or len(email) == 0 or not email_valido(email):
            flash('ERROR: Debe suministrar un email válido')
            swerror = True
        if password == None or len(password) == 0 or not pass_valido(password):
            flash('ERROR: Debe suministrar una clave válida')
            swerror = True
        if confirm == None or len(confirm) == 0 or not pass_valido(confirm):
            flash('ERROR: Debe suministrar una verificación de clave válida')
            swerror = True
        if password != confirm:
            flash('ERROR: La clave y la confirmación no coinciden')
            swerror = True
        if not swerror:
            # Preparar la consulta
            sql = 'INSERT INTO Paciente(nombres, Apellidos, tipoId, NumeroId, fechaNacimiento, sexo, grupoSanguineo, mail, telefono, usuario, clave, idrol) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
            # Ejecutar la consulta
            pwd = generate_password_hash(password)  # Cifrar la clave
            res = accion(sql, (name, lastname, tipoid, id, birthdate,
                         sex, rh, email, phonenumber, username, pwd, role))
            # Verificar resultados
            if res == 0:
                flash('ERROR: No se pudo insertar el registro')
            else:
                flash(
                    'Atualización: Datos grabados con exito. Para acceder ingrese sus credenciales.')
                return redirect(url_for('login'))

        return render_template('forms/registropac.html', form=pacform)


@app.route('/registromed', methods=['GET', 'POST'])
def registromed():
    medform = RegisterFormMed(request.form)
    if request.method == 'GET':
        return render_template('forms/registromed.html', form=medform)
    else:
        # Recuperar los datos del formulario
        name = escape(request.form['name'])
        lastname = escape(request.form['lastname'])
        tipoid = escape(request.form['tipoid'])
        id = escape(request.form['id'])
        specialty = escape(request.form['specialty'])
        birthdate = escape(request.form['birthdate'])
        sex = escape(request.form['sex'])
        rh = escape(request.form['rh'])
        modalidad = escape(request.form['modalidad'])
        email = escape(request.form['email'])
        professionalId = escape(request.form['professionalId'])
        phonenumber = escape(request.form['phonenumber'])
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        confirm = escape(request.form['confirm'])
        role = 2
        # Validar los datos
        swerror = False
        if name == None or len(name) == 0:
            flash('ERROR: Debe suministrar el nombre del medico')
            swerror = True
        if lastname == None or len(lastname) == 0:
            flash('ERROR: Debe suministrar el apellido del medico')
            swerror = True
        if tipoid == None or len(tipoid) == 0:
            flash('ERROR: Debe suministrar el tipo de documento')
            swerror = True
        if id == None or len(id) == 0:
            flash('ERROR: Debe suministrar un numero de identificación')
            swerror = True
        if specialty == None or len(specialty) == 0:
            flash('ERROR: Debe suministrar la especialidad del médico')
            swerror = True
        if modalidad == None or len(modalidad) == 0:
            flash('ERROR: Debe suministrar la jornada de trabajo del médico')
            swerror = True
        if username == None or len(username) == 0 or not login_valido(username):
            flash('ERROR: Debe suministrar un usuario válido ')
            swerror = True
        if email == None or len(email) == 0 or not email_valido(email):
            flash('ERROR: Debe suministrar un email válido')
            swerror = True
        if password == None or len(password) == 0 or not pass_valido(password):
            flash('ERROR: Debe suministrar una clave válida')
            swerror = True
        if confirm == None or len(confirm) == 0 or not pass_valido(confirm):
            flash('ERROR: Debe suministrar una verificación de clave válida')
            swerror = True
        if password != confirm:
            flash('ERROR: La clave y la confirmación no coinciden')
            swerror = True
        if not swerror:
            # Preparar la consulta
            pwd = generate_password_hash(password)  # Cifrar la clave
            sql = 'INSERT INTO Médico(nombres,apellidos,tipoId,NumeroId,idespecialidad,fechaNacimiento,sexo,grupoSanguineo,modalidad,mail,tarjetaProfesional,teléfono,usuario,clave,idrol) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            res = accion(sql, (name, lastname, tipoid, id, specialty, birthdate, sex,
                         rh, modalidad, email, professionalId, phonenumber, username, pwd, role))
            # Verificar resultados
            if res == 0:
                flash('ERROR: No se pudo insertar el registro')
            else:
                flash(
                    'Atualización: Datos grabados con exito. Para acceder ingrese sus credenciales.')
                return redirect(url_for('login'))

        return render_template('forms/registromed.html', form=medform)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/wedit', methods=['GET', 'POST'])
def vistaCita():
    if session:
        if session['rol'] == '1':
            rol = session['rol']
        elif session['rol'] == '2':
            rol = session['rol']
        else:
            rol = session['rol']

        if request.method == 'GET':
            jsdata = request.args.get('jsdata')
            print("jsdata: "+jsdata)

            # Preparar la consulta
            sqlcita = f"SELECT idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion, id FROM Cita WHERE id = '{jsdata}'"
            # Ejecutar la consulta
            rescita = seleccion(sqlcita)

            sqlmed = f"SELECT nombres, apellidos FROM Médico WHERE idmedico = '{rescita[0][2]}'"
            sqlpac = f"SELECT nombres, apellidos FROM Paciente WHERE idpaciente = '{rescita[0][0]}'"
            resmed = seleccion(sqlmed)
            respac = seleccion(sqlpac)
            datos = {
                "id": rescita[0][7],
                "descrip": rescita[0][1],
                "paciente": respac[0][0]+" "+respac[0][1],
                "idp": rescita[0][0],
                "doctor": resmed[0][0]+" "+resmed[0][1],
                "idd": rescita[0][2],
                "fecha": rescita[0][3]+" "+rescita[0][4],
                "comentario": rescita[0][5],
                "valoracion": rescita[0][6],
                "rol": rol
            }

            return render_template('pages/wedit.html', data=datos)
    else:
        return render_template('pages/invalid.html')


@app.route('/lista/', methods=['GET', 'POST'])
def lista():
    if session:
        if request.method == 'GET':
            if session["rol"] != '1':
                datos = []
                # Preparar la consulta
                sqlcita = f"SELECT idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion, id FROM Cita"
                # Ejecutar la consulta
                rescita = seleccion(sqlcita)

                i = 0
                while i < len(rescita):
                    sqlmed = f"SELECT nombres, apellidos FROM Médico WHERE idmedico = '{rescita[i][2]}'"
                    sqlpac = f"SELECT nombres, apellidos FROM Paciente WHERE idpaciente = '{rescita[i][0]}'"
                    resmed = seleccion(sqlmed)
                    respac = seleccion(sqlpac)
                    temp = {
                        "index": i+1,
                        "descrip": rescita[i][1],
                        "paciente": respac[0][0]+" "+respac[0][1],
                        "idp": rescita[i][0],
                        "id": rescita[i][7],
                        "doctor": resmed[0][0]+" "+resmed[0][1],
                        "idd": rescita[i][2],
                        "fecha": rescita[i][3]+" "+rescita[i][4],
                        "comentario": rescita[i][5],
                        "valoracion": rescita[i][6]
                    }
                    datos.append(temp)
                    i += 1
                return render_template('pages/lista.html', data=datos)
            else:
                datos = []
                # Preparar la consulta
                sqlpac = f"SELECT idpaciente FROM Paciente WHERE usuario = '{session['usr']}'"
                #Ejecutar la consulta
                respac = seleccion(sqlpac)
                #Preparar la consulta
                sqlcita = f"SELECT idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion, id FROM Cita WHERE idpaciente = '{respac[0][0]}'"
                # Ejecutar la consulta
                rescita = seleccion(sqlcita)

                i = 0
                while i < len(rescita):
                    sqlmed = f"SELECT nombres, apellidos FROM Médico WHERE idmedico = '{rescita[i][2]}'"
                    sqlpac = f"SELECT nombres, apellidos FROM Paciente WHERE idpaciente = '{rescita[i][0]}'"
                    resmed = seleccion(sqlmed)
                    respac = seleccion(sqlpac)
                    temp = {
                        "index": i+1,
                        "descrip": rescita[i][1],
                        "paciente": respac[0][0]+" "+respac[0][1],
                        "idp": rescita[i][0],
                        "id": rescita[i][7],
                        "doctor": resmed[0][0]+" "+resmed[0][1],
                        "idd": rescita[i][2],
                        "fecha": rescita[i][3]+" "+rescita[i][4],
                        "comentario": rescita[i][5],
                        "valoracion": rescita[i][6]
                    }
                    datos.append(temp)
                    i += 1
                return render_template('pages/lista.html', data=datos)
    else:
        return render_template('pages/invalid.html')


@app.route('/dashboard')
# @login_required
# Con el condicional se aseguran de que la vista se renderiza solo si el usuario está logueado
def dashboard():
    # usr_id = 'usr_id' in session
    # if usr_id:
    form = DashBoardMedico(request.form)
    return render_template('forms/dashboard-medico.html', form=form)
    # elif session['usr_id'] == 'testmed123':
    #     form = DashBoardPaciente(request.form)
    #     return render_template('forms/dashboard-paciente.html', form=form)
    # elif session['usr_id'] == 'testadmin123':
    #     form = DashBoardAdmin(request.form)
    #     return render_template('forms/dashboard-admin.html', form=form)
    # elif session['usr_id'] == 'testmed123':
    #     form = DashBoardMedico(request.form)
    #     return render_template('forms/dashboard-medico.html', form=form)
    # else:
    #     return render_template('pages/invalid.html')

@app.route('/citasFormRequest', methods=['GET', 'POST'])
def citasRequest():
    if request.method == 'GET':
        jsdata3 = request.args.get('jsdata3')
        data = []
        if(jsdata3 == '1'):
            jsdata1 = request.args.get('jsdata1')
            # Preparar la consulta
            sql = f"SELECT nombres, apellidos, modalidad FROM Médico WHERE idespecialidad = '{jsdata1}'"
            # Ejecutar la consulta
            res = seleccion(sql)
            
            if res:
                i = 0
                while i < len(res):
                    temp = {"nombres": res[i][0],
                            "apellidos": res[i][1],
                            "modalidad": res[i][2],
                            "found": "true"}
                    i += 1
                    data.append(temp)    
            else:
                data = [{"found": "false"}]
        elif(jsdata3 == '2'):
            jsdata1 = request.args.get('jsdata1')
            jsdata2 = request.args.get('jsdata2')
            # Preparar la consulta
            sql = f"SELECT modalidad FROM Médico WHERE nombres = '{jsdata1}' and apellidos = '{jsdata2}'"
            # Ejecutar la consulta
            res = seleccion(sql)
            # Preparar la consulta
            sqlhora = f"SELECT horario FROM Horario WHERE modalidad = '{res[0][0]}'"
            # Ejecutar la consulta
            reshora = seleccion(sqlhora)
            if reshora:
                i = 0
                while i < len(reshora):
                    temp = {
                        "horario": reshora[i][0],
                        "modalidad": res[0][0]
                    }
                    data.append(temp)
                    i += 1
        elif(jsdata3 == '3'):
            jsdata1 = request.args.get('jsdata1')            
            # Preparar la consulta
            sql = f"SELECT nombres, Apellidos, tipoId, mail FROM Paciente WHERE NumeroId LIKE '{jsdata1}'"
            # Ejecutar la consulta
            res = seleccion(sql)
            
            if res:
                temp = {
                        "tipoid": res[0][2],
                        "paciente": res[0][0],
                        "apellido": res[0][1],
                        "email": res[0][3],
                        "found": "true"
                    }
                data.append(temp)
            else:
                data = [{"found": "false"}]
        elif(jsdata3 == '4'):
            jsdata1 = request.args.get('jsdata1')
            jsdata2 = request.args.get('jsdata2')            
            # Preparar la consulta
            sql = f"SELECT numeroId FROM Médico WHERE nombres = '{jsdata1}' and apellidos = '{jsdata2}'"
            # Ejecutar la consulta
            res = seleccion(sql)
            
            if res:
                temp = {
                        "idmedico": res[0][0],
                        "found": "true"
                    }
                data.append(temp)
            else:
                data = [{"found": "false"}]
    return jsonify(data)

@app.route('/citasForm', methods=['GET', 'POST'])
# Con el condicional se aseguran de que la vista se renderiza solo si el usuario está logueado
def citas():
    if request.method == 'GET':
        form = CitaForm(request.form)
        return render_template('forms/citasForm.html', form=form)
    elif request.method == 'POST':
        # Recuperar los datos del formulario
        idp = escape(request.form['id_paciente'])
        especialidad = escape(request.form['especialidad'])        
        idm = escape(request.form['idm'])
        hora = escape(request.form['time'])
        fecha = escape(request.form['fecha'])
        comentario = escape(request.form['comentario'])
        valoracion = escape(request.form['valoracion'])
        # Preparar la consulta
        #Recuperar Ids de BD
        sqlidmed = f"SELECT idmedico FROM Médico WHERE numeroId = '{idm}'"
        sqlidpac = f"SELECT idpaciente FROM Paciente WHERE NumeroId = '{idp}'"
        residmed = seleccion(sqlidmed)
        residpac = seleccion(sqlidpac)
        # Preparar la consulta
        sql = "INSERT INTO Cita(idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion) VALUES (?,?,?,?,?,?,?)"
        res = accion(sql, (residpac[0][0], especialidad, residmed[0][0],
                     hora, fecha, comentario, valoracion))
        # Verificar resultados
        if res == 0:
            flash('ERROR: No se pudo insertar el registro')
        else:
            flash('Atualización: Datos grabados con exito en la BD.')
        return redirect(url_for('lista'))

# rutas del dashboard administrativo


@app.route('/Dashboard-Admin/')
def DashboardAdmin():
    if request.method == 'GET':
        return render_template('forms/DashboardAdmin.html')


@app.route('/pacientes/', methods=['GET', 'POST'])
def pacientes():
    frm = Paciente()
    if request.method == 'GET':
        return render_template('forms/pacientes.html', form=frm)


@app.route('/vistamedico/', methods=['GET', 'POST'])
def vistamedico():
    frm = DashBoardMedico()
    if request.method == 'GET':
        return render_template('forms/dashboard-medico.html', form=frm)


@app.route('/vistacitas/', methods=['GET', 'POST'])
def vistacitas():
    frm = Cita()
    if request.method == 'GET':
        return render_template('forms/dashboard-citas.html', form=frm)


@app.route('/get/')
def get():
    return session.get('rol', 'not set')

# RUTA VÁLIDA SOLO PARA PACIENTES POR EL MOMENTO


@app.route('/perfil/', methods=['GET', 'POST'])
def perfil():
    frm = Perfil(request.form)
    usuario = session['usr']
    if request.method == 'GET':
        # if session['rol'] == 1:
        # if 'rol' in session:
        #     if session['rol'] == 1:
        # Preparar la consulta
        sql = f"SELECT mail, usuario, clave FROM Paciente WHERE usuario='{usuario}'"
        # Ejecutar la consulta
        res = seleccion(sql)
        # Proceso los resultados
        if len(res) == 0:
            tit = f"No se encontraron datos para : {session['usr']}"
        else:
            tit = f"Se muestran los datos para : {session['usr']}"
            frm = Perfil()
        return render_template('forms/perfil.html', form=frm, titulo=tit, data=res)
    else:
        # Recuperar datos del usuario de la sesion
        # Recuperar los datos del formulario
        # Esta forma permite validar las entradas
        if request.form.get('action1') == 'Actualizar correo electrónico':
            # usr = escape(request.form['usr'])
            mailUsuario = escape(request.form['mailUsuario'])
            # pwd = escape(request.form['pwd'])
            # Validar los datos
            swerror = False
            # if usr == None or len(usr) == 0 or not login_valido(usr):
            #     flash('ERROR: Debe suministrar un usuario válido ')
            #     swerror = True
            if mailUsuario == None or len(mailUsuario) == 0 or not email_valido(mailUsuario):
                flash('ERROR: Debe suministrar un email válido')
                swerror = True
            if not swerror:
                sql = f"SELECT mail, usuario, clave FROM Paciente WHERE usuario='{usuario}'"
                # Ejecutar la consulta
                res = seleccion(sql)
                # Proceso los resultados
                # Preparar el query -- Paramétrico
                sql2 = f"UPDATE Paciente set mail = ? where usuario = ?"
                # Ejecutar la consulta
                # pwd = generate_password_hash(pwd)
                res2 = accion(sql2, (mailUsuario, usuario))
                if res2 == 0:
                    flash('ERROR: No se pudieron almacenar los datos, reintente')
                else:
                    flash('INFO: Los datos fueron almacenados satisfactoriamente')
        elif request.form.get('action2') == 'Actualizar usuario':
            newusr = escape(request.form['usr'])
            # Validar los datos
            swerror = False
            if newusr == None or len(newusr) == 0 or not pass_valido(newusr):
                flash('ERROR: Debe suministrar una clave válida')
                swerror = True
            if not swerror:
                sql = f"SELECT mail, usuario, clave FROM Paciente WHERE usuario='{usuario}'"
                # Ejecutar la consulta
                res = seleccion(sql)
                # Proceso los resultados
                # Preparar el query -- Paramétrico
                sql2 = f"UPDATE Paciente set usuario = ? where usuario = ?"
                # Ejecutar la consulta
                # pwd = generate_password_hash(pwd)
                res2 = accion(sql2, (newusr, usuario))
                if res2 == 0:
                    flash('ERROR: No se pudieron almacenar los datos, reintente')
                else:
                    session['usr'] = newusr
                    flash('INFO: Los datos fueron almacenados satisfactoriamente')
        elif request.form.get('action3') == 'Actualizar contraseña':
            newpwd = escape(request.form['pwd'])
            confirm = escape(request.form['confirm'])
            swerror = False
            sql = f"SELECT mail, usuario, clave FROM Paciente WHERE usuario='{usuario}'"
            # Ejecutar la consulta
            res = seleccion(sql)
            # Validar los datos
            if newpwd == None or len(newpwd) == 0 or not pass_valido(newpwd):
                flash('ERROR: Debe suministrar una clave válida')
                swerror = True
            if confirm == None or len(confirm) == 0 or not pass_valido(confirm):
                flash('ERROR: Debe suministrar una verificación de clave válida')
                swerror = True
            if newpwd != confirm:
                flash('ERROR: La clave y la confirmación no coinciden')
                swerror = True
            if not swerror:
                # Proceso los resultados
                # Preparar el query -- Paramétrico
                sql2 = f"UPDATE Paciente set clave = ? where usuario = ?"
                # Ejecutar la consulta
                pwd = generate_password_hash(newpwd)
                res2 = accion(sql2, (pwd, usuario))
                if res2 == 0:
                    flash('ERROR: No se pudieron almacenar los datos, reintente')
                else:
                    flash('INFO: Los datos fueron almacenados satisfactoriamente')
        return render_template('forms/perfil.html', form=frm, data=res)
    # elif session['rol'] == 2:
    #     # Preparar la consulta
    #     sql = f'SELECT mail, usuario, clave FROM Medico WHERE usuario = {usuario}'
    #     # Ejecutar la consulta
    #     res = seleccion(sql)
    #     # Proceso los resultados
    #     if len(res) == 0:
    #         tit = f"No se encontraron datos para : {session['usr']}"
    #     else:
    #         tit = f"Se muestran los datos para : {session['usr']}"
    #     return render_template('forms/perfil.html', form=frm, titulo=tit, data=res)
    # elif session['rol'] == 3:
    #     # Preparar la consulta
    #     sql = f'SELECT mail, usuario, clave FROM Superusuario WHERE usuario = {usuario}'
    #     # Ejecutar la consulta
    #     res = seleccion(sql)
    #     # Proceso los resultados
    #     if len(res) == 0:
    #         tit = f"No se encontraron datos para : {session['usr']}"
    #     else:
    #         tit = f"Se muestran los datos para : {session['usr']}"
    #     return render_template('forms/perfil.html', form=frm, titulo=tit, data=res)
    # return render_template('forms/perfil.html', form=frm)
    # else:
    #     # Recuperar datos del usuario de la sesion
    #     # Recuperar los datos del formulario
    #     # Esta forma permite validar las entradas
    #     usr = escape(request.form['usr'])
    #     mailUsuario = escape(request.form['mailUsuario'])
    #     pwd = escape(request.form['pwd'])
    #     # Validar los datos
    #     swerror = False
    #     if usr == None or len(usr) == 0 or not login_valido(usr):
    #         flash('ERROR: Debe suministrar un usuario válido ')
    #         swerror = True
    #     if mailUsuario == None or len(mailUsuario) == 0 or not email_valido(mailUsuario):
    #         flash('ERROR: Debe suministrar un email válido')
    #         swerror = True
    #     if pwd == None or len(pwd) == 0 or not pass_valido(pwd):
    #         flash('ERROR: Debe suministrar una clave válida')
    #         swerror = True
    #     if not swerror:
    #         # Preparar el query -- Paramétrico
    #         sql = "INSERT INTO usuario(usuario, correo, clave) VALUES(?, ?, ?)"
    #         # Ejecutar la consulta
    #         pwd = generate_password_hash(pwd)
    #         res = accion(sql, (usr, mailUsuario, pwd))
    #         # Proceso los resultados
    #         if res == 0:
    #             flash('ERROR: No se pudieron almacenar los datos, reintente')
    #         else:
    #             flash('INFO: Los datos fueron almacenados satisfactoriamente')
    #     return render_template('mensajes.html', data=res)


@app.route('/vistaBusquedas/', methods=['GET', 'POST'])
def vistaBusquedas():
    frm = VistaBusquedas()
    if request.method == 'GET':
        return render_template('forms/vistaBusquedas.html', form=frm)


@app.route('/logout/')
def logout():
    session.clear()
    return render_template('pages/placeholder.home.html')

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
'''
