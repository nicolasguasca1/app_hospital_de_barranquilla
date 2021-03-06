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
from db import accion, borrar, seleccion
import datetime
from datetime import datetime

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
    form = LoginForm(request.form)
    if 'usr' in session:
        return redirect(url_for('home'))
    elif request.method == 'GET' and 'usr' not in session:
        return render_template('forms/login.html', form=form)
    else:
        # Recuperar los datos
        usr = escape(form.usr.data.strip())
        pwd = escape(form.pwd.data.strip())
        # Validar los datos
        swvalido = True
        # if len(usr) < 6 or len(usr) > 40:
        #     swvalido = False
        #     flash(
        #         "El nombre de usuario es requerido y tiene entre 6 y 40 caracteres", 'error')
        # if len(pwd) < 6 or len(pwd) > 40:
        #     swvalido = False
        #     flash("El nombre de usuario es requerido y tiene entre 6 y 40 caracteres")
        # Preparar la consulta
        sqlmed = f"SELECT idmedico, nombres, mail, clave, idrol FROM M??dico WHERE usuario = '{usr}'"
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
                flash('ERROR: Usuario o clave invalidos', 'error')
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
                flash('ERROR: Usuario o clave invalidos', 'error')
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
                flash('ERROR: Usuario o clave invalidos', 'error')
                return render_template('forms/login.html', form=form)

        # elif form.btn():
        #     login_user(user)
        #     flash('Ha iniciado sesi??n correctamente.')
        else:
            flash('ERROR: Usuario o clave invalidos', 'error')
            return render_template('forms/login.html', form=form)


@app.route('/registropac', methods=['GET', 'POST'])
def registropac():
    pacform = RegisterFormPac(request.form)
    if 'usr' in session:
        return render_template('errors/logueado.html')
    elif request.method == 'GET':
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
            flash(
                'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
            swerror = True
        if username == None or len(username) == 0 or not login_valido(username):
            flash('ADVERTENCIA: Debe suministrar un usuario v??lido ', 'advertencia')
            swerror = True
        if email == None or len(email) == 0 or not email_valido(email):
            flash('ADVERTENCIA: Debe suministrar un email v??lido', 'advertencia')
            swerror = True
        if password == None or len(password) == 0 or not pass_valido(password):
            flash('ADVERTENCIA: Debe suministrar una clave v??lida', 'advertencia')
            swerror = True
        if confirm == None or len(confirm) == 0 or not pass_valido(confirm):
            flash(
                'ADVERTENCIA: Debe suministrar una verificaci??n de clave v??lida', 'advertencia')
            swerror = True
        if password != confirm:
            flash('ADVERTENCIA: La clave y la confirmaci??n no coinciden', 'advertencia')
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
                    'Datos grabados con exito. Para acceder ingrese sus credenciales.', 'actualiza')
                return redirect(url_for('login'))

        return render_template('forms/registropac.html', form=pacform)


@app.route('/registromed', methods=['GET', 'POST'])
def registromed():
    medform = RegisterFormMed(request.form)
    if 'usr' in session:
        return render_template('errors/logueado.html')
    elif request.method == 'GET':
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
            flash('ADVERTENCIA: Debe suministrar el nombre del medico', 'advertencia')
            swerror = True
        if lastname == None or len(lastname) == 0:
            flash('ADVERTENCIA: Debe suministrar el apellido del medico', 'advertencia')
            swerror = True
        if tipoid == None or len(tipoid) == 0:
            flash('ADVERTENCIA: Debe suministrar el tipo de documento', 'advertencia')
            swerror = True
        if id == None or len(id) == 0:
            flash(
                'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
            swerror = True
        if specialty == None or len(specialty) == 0:
            flash(
                'ADVERTENCIA: Debe suministrar la especialidad del m??dico', 'advertencia')
            swerror = True
        if modalidad == None or len(modalidad) == 0:
            flash(
                'ADVERTENCIA: Debe suministrar la jornada de trabajo del m??dico', 'advertencia')
            swerror = True
        if username == None or len(username) == 0 or not login_valido(username):
            flash('ADVERTENCIA: Debe suministrar un usuario v??lido ', 'advertencia')
            swerror = True
        if email == None or len(email) == 0 or not email_valido(email):
            flash('ADVERTENCIA: Debe suministrar un email v??lido', 'advertencia')
            swerror = True
        if password == None or len(password) == 0 or not pass_valido(password):
            flash('ADVERTENCIA: Debe suministrar una clave v??lida', 'advertencia')
            swerror = True
        if confirm == None or len(confirm) == 0 or not pass_valido(confirm):
            flash(
                'ADVERTENCIA: Debe suministrar una verificaci??n de clave v??lida', 'advertencia')
            swerror = True
        if password != confirm:
            flash('ADVERTENCIA: La clave y la confirmaci??n no coinciden', 'advertencia')
            swerror = True
        if not swerror:
            # Preparar la consulta
            pwd = generate_password_hash(password)  # Cifrar la clave
            sql = 'INSERT INTO M??dico(nombres,apellidos,tipoId,NumeroId,idespecialidad,fechaNacimiento,sexo,grupoSanguineo,modalidad,mail,tarjetaProfesional,tel??fono,usuario,clave,idrol) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            res = accion(sql, (name, lastname, tipoid, id, specialty, birthdate, sex,
                         rh, modalidad, email, professionalId, phonenumber, username, pwd, role))
            # Verificar resultados
            if res == 0:
                flash('ERROR: No se pudo insertar el registro', 'error')
            else:
                flash(
                    'Datos grabados con exito. Para acceder ingrese sus credenciales.', 'actualiza')
                return redirect(url_for('login'))

        return render_template('forms/registromed.html', form=medform)


@app.route('/forgot')
def forgot():
    if 'usr' in session:
        return redirect(url_for('home'))
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
            jsdata1 = request.args.get('jsdata1')
            if jsdata1 != '1':
                # Preparar la consulta
                sqlcita = f"SELECT idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion, id FROM Cita WHERE id = '{jsdata}'"

                # Ejecutar la consulta
                rescita = seleccion(sqlcita)
                fecha_split = str(rescita[0][4]).split("-")
                fecha_cita = datetime(int(fecha_split[0]), int(
                    fecha_split[1]), int(fecha_split[2]))
                fecha_hoy = datetime.now()  # fecha de hoy
                # Consultar valoracion
                sqlval = f"SELECT Valoracion FROM Valoraciones WHERE id = '{rescita[0][6]}'"
                resval = seleccion(sqlval)
                if resval:
                    val = resval[0][0]
                else:
                    val = ""

                if (fecha_cita < fecha_hoy):
                    ontime = 1
                else:
                    ontime = 0
                sqlmed = f"SELECT nombres, apellidos FROM M??dico WHERE idmedico = '{rescita[0][2]}'"
                sqlpac = f"SELECT nombres, apellidos FROM Paciente WHERE idpaciente = '{rescita[0][0]}'"
                resmed = seleccion(sqlmed)
                respac = seleccion(sqlpac)
                datos = {
                    "id": rescita[0][7],
                    "descrip": rescita[0][1],
                    "paciente": str(respac[0][0])+" "+str(respac[0][1]),
                    "idp": rescita[0][0],
                    "doctor": str(resmed[0][0])+" "+str(resmed[0][1]),
                    "idd": rescita[0][2],
                    "fecha": str(rescita[0][3])+" "+str(rescita[0][4]),
                    "comentario": rescita[0][5],
                    "valoracion": val,
                    "rol": rol,
                    "ontime": ontime,
                    "edicion": '0'
                }
                return render_template('pages/wedit.html', data=datos)
            else:
                # Preparar la consulta
                sqlcita = f"SELECT idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion, id FROM Cita WHERE id = '{jsdata}'"
                # Ejecutar la consulta
                rescita = seleccion(sqlcita)
                fecha_split = str(rescita[0][4]).split("-")
                fecha_cita = datetime(int(fecha_split[0]), int(
                    fecha_split[1]), int(fecha_split[2]))
                fecha_hoy = datetime.now()  # fecha de hoy
                # Consultar valoracion
                sqlval = f"SELECT Valoracion FROM Valoraciones WHERE id = '{rescita[0][6]}'"
                resval = seleccion(sqlval)
                if resval:
                    val = resval[0][0]
                else:
                    val = ""

                if (fecha_cita < fecha_hoy):
                    ontime = 1
                else:
                    ontime = 0
                sqlmed = f"SELECT nombres, apellidos FROM M??dico WHERE idmedico = '{rescita[0][2]}'"
                sqlpac = f"SELECT nombres, apellidos FROM Paciente WHERE idpaciente = '{rescita[0][0]}'"
                resmed = seleccion(sqlmed)
                respac = seleccion(sqlpac)
                datos = {
                    "id": rescita[0][7],
                    "descrip": rescita[0][1],
                    "paciente": str(respac[0][0])+" "+str(respac[0][1]),
                    "idp": rescita[0][0],
                    "doctor": str(resmed[0][0])+" "+str(resmed[0][1]),
                    "idd": rescita[0][2],
                    "fecha": str(rescita[0][3])+" "+str(rescita[0][4]),
                    "comentario": rescita[0][5],
                    "valoracion": val,
                    "rol": rol,
                    "ontime": ontime,
                    "edicion": '1'
                }
                return render_template('pages/wedit.html', data=datos)
        else:
            if request.form['rol'] == '1':
                jsdata = request.form['valoracion']
            elif request.form['rol'] == '2':
                jsdata1 = request.form['comentario']
            else:
                jsdata = request.form['valoracion']
                jsdata1 = request.form['comentario']
            jsdata2 = request.form['id']

            if request.form['rol'] == '1':
                sql = f"UPDATE Cita SET valoracion = ? WHERE id = ?"
                res = accion(sql, (jsdata, jsdata2))
            elif request.form['rol'] == '2':
                sql = f"UPDATE Cita SET comentarios = ? WHERE id = ?"
                res = accion(sql, (jsdata1, jsdata2))
            else:
                sql = f"UPDATE Cita SET comentarios = ?, valoracion = ? WHERE id = ?"
                res = accion(sql, (jsdata1, jsdata, jsdata2))
            if res == 0:
                flash('ERROR: No se pudo actualizar el registro', 'error')
            else:
                flash("El registro se ha actualizado", 'actualiza')
            return redirect(url_for('lista'))
    else:
        return render_template('error/no_logueado.html')


@app.route('/lista/', methods=['GET', 'POST'])
def lista():
    if session:
        if request.method == 'GET':
            if session["rol"] == '3':
                datos = []
                # Preparar la consulta
                sqlcita = f"SELECT idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion, id, Estado FROM Cita"
                # Ejecutar la consulta
                rescita = seleccion(sqlcita)
                i = 0
                while i < len(rescita):
                    sqlmed = f"SELECT nombres, apellidos FROM M??dico WHERE idmedico = '{rescita[i][2]}'"
                    sqlpac = f"SELECT nombres, apellidos FROM Paciente WHERE idpaciente = '{rescita[i][0]}'"
                    resmed = seleccion(sqlmed)
                    respac = seleccion(sqlpac)
                    temp = {
                        "index": i+1,
                        "descrip": rescita[i][1],
                        "paciente": str(respac[0][0])+" "+str(respac[0][1]),
                        "idp": rescita[i][0],
                        "id": rescita[i][7],
                        "doctor": str(resmed[0][0])+" "+str(resmed[0][1]),
                        "idd": rescita[i][2],
                        "fecha": rescita[i][4],
                        "hora": rescita[i][3],
                        "comentario": rescita[i][5],
                        "valoracion": rescita[i][6],
                        "estado": rescita[i][8]
                    }
                    datos.append(temp)
                    datos = sorted(datos, key=lambda d: d['fecha'])
                    i += 1
                return render_template('pages/lista.html', data=datos)
            elif session["rol"] == '2':
                datos = []
                # Preparar la consulta
                sqlpac = f"SELECT idmedico FROM M??dico WHERE usuario = '{session['usr']}'"
                # Ejecutar la consulta
                respac = seleccion(sqlpac)
                # Preparar la consulta
                sqlcita = f"SELECT idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion, id FROM Cita WHERE idmedico = '{respac[0][0]}' and Estado = 'ACTIVO'"
                # Ejecutar la consulta
                rescita = seleccion(sqlcita)

                i = 0
                while i < len(rescita):
                    sqlmed = f"SELECT nombres, apellidos FROM M??dico WHERE idmedico = '{rescita[i][2]}'"
                    sqlpac = f"SELECT nombres, apellidos FROM Paciente WHERE idpaciente = '{rescita[i][0]}'"
                    resmed = seleccion(sqlmed)
                    respac = seleccion(sqlpac)
                    temp = {
                        "index": i+1,
                        "descrip": rescita[i][1],
                        "paciente": str(respac[0][0])+" "+str(respac[0][1]),
                        "idp": rescita[i][0],
                        "id": rescita[i][7],
                        "doctor": str(resmed[0][0])+" "+str(resmed[0][1]),
                        "idd": rescita[i][2],
                        "fecha": rescita[i][4],
                        "hora": rescita[i][3],
                        "comentario": rescita[i][5],
                        "valoracion": rescita[i][6]
                    }
                    datos.append(temp)
                    datos = sorted(datos, key=lambda d: d['fecha'])
                    i += 1
                return render_template('pages/lista.html', data=datos)
            else:
                datos = []
                # Preparar la consulta
                sqlpac = f"SELECT idpaciente FROM Paciente WHERE usuario = '{session['usr']}'"
                # Ejecutar la consulta
                respac = seleccion(sqlpac)
                # Preparar la consulta
                sqlcita = f"SELECT idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion, id FROM Cita WHERE idpaciente = '{respac[0][0]}' and Estado = 'ACTIVO'"
                # Ejecutar la consulta
                rescita = seleccion(sqlcita)

                i = 0
                while i < len(rescita):
                    sqlmed = f"SELECT nombres, apellidos FROM M??dico WHERE idmedico = '{rescita[i][2]}'"
                    sqlpac = f"SELECT nombres, apellidos FROM Paciente WHERE idpaciente = '{rescita[i][0]}'"
                    resmed = seleccion(sqlmed)
                    respac = seleccion(sqlpac)
                    temp = {
                        "index": i+1,
                        "descrip": rescita[i][1],
                        "paciente": str(respac[0][0])+" "+str(respac[0][1]),
                        "idp": rescita[i][0],
                        "id": rescita[i][7],
                        "doctor": str(resmed[0][0])+" "+str(resmed[0][1]),
                        "idd": rescita[i][2],
                        "fecha": rescita[i][4],
                        "hora": rescita[i][3],
                        "comentario": rescita[i][5],
                        "valoracion": rescita[i][6]
                    }
                    datos.append(temp)
                    datos = sorted(datos, key=lambda d: d['fecha'])
                    i += 1
                return render_template('pages/lista.html', data=datos)
    else:
        return render_template('pages/invalid.html')


@app.route('/borrarCita', methods=['GET', 'POST'])
def borrarCita():
    if request.method == 'POST':
        jsdata = request.form['data']
        estado = "INACTIVO"
        sql = f"UPDATE Cita set Estado = ? where id = ?"
        res = accion(sql, (estado, jsdata))
        if res == 0:
            flash('ERROR: No se pudo borrar el registro', 'error')
        else:
            flash("INFO: El registro se ha borrado", 'info')
        return redirect(url_for('lista'))


@app.route('/borrarcitasForm', methods=['GET'])
def borrarForm():
    if request.method == 'GET':
        jsdata = request.args.get('jsdata')
        return render_template('forms/borrarCitaForm.html', data=jsdata)


@app.route('/citasFormRequest', methods=['GET', 'POST'])
def citasRequest():
    if request.method == 'GET':
        jsdata3 = request.args.get('jsdata3')
        data = []
        if(jsdata3 == '1'):
            jsdata1 = request.args.get('jsdata1')
            # Preparar la consulta
            sql = f"SELECT nombres, apellidos, modalidad FROM M??dico WHERE idespecialidad = '{jsdata1}'"
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
            jsdata4 = request.args.get('jsdata4')  # fecha seleccionada
            fecha_hoy = str(datetime.now().strftime(
                '%Y-%m-%d'))  # fecha de hoy

            # Preparar la consulta modalidad del medico
            sql = f"SELECT modalidad, idmedico FROM M??dico WHERE nombres = '{jsdata1}' and apellidos = '{jsdata2}'"
            # Ejecutar la consulta
            res = seleccion(sql)
            # consultar horarios de citas del medico en la fecha seleccionada
            if(jsdata4 != ""):
                sqlcita = f"SELECT horario FROM Cita WHERE idmedico = '{res[0][1]}' and fecha = '{jsdata4}'"
            else:
                sqlcita = f"SELECT horario FROM Cita WHERE idmedico = '{res[0][1]}' and fecha = '{fecha_hoy}'"
            print(sqlcita)
            rescita = seleccion(sqlcita)
            print(rescita)
            # Preparar la consulta horarios segun modalidad
            sqlhora = f"SELECT horario FROM Horario WHERE modalidad = '{res[0][0]}'"
            # Ejecutar la consulta
            reshora = seleccion(sqlhora)
            if reshora:
                i = 0
                sw = 0
                while i < len(reshora):
                    if rescita:
                        j = 0
                        while j < len(rescita):
                            if(rescita[j][0] == reshora[i][0]):
                                sw = 1
                            j += 1
                    if(sw == 0):
                        temp = {
                            "horario": reshora[i][0],
                            "modalidad": res[0][0]
                        }
                        data.append(temp)
                    sw = 0
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
            sql = f"SELECT numeroId FROM M??dico WHERE nombres = '{jsdata1}' and apellidos = '{jsdata2}'"
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


@app.route('/dashboard/medico', methods=['GET', 'POST'])
def dashboardmedico():
    if session:
        if session.get('rol') == '3':
            form = DashBoardMedico(request.form)
            if request.method == 'GET':
                session['tipoid'] = ""
                session['txtNroDoc'] = ""
                session['nombres'] = ""
                session['apellidos'] = ""
                session['mail'] = ""
                session['telefono'] = ""
                session['usuario'] = ""
                session['clave'] = ""
                session['found'] = False
                return render_template('forms/dashboard-medico.html', form=form)
            else:
                if request.form.get('regbtn') == 'Crear Registro':
                    name = escape(request.form['name'])
                    lastname = escape(request.form['last'])
                    tipoid = escape(request.form['tipoid'])
                    id = escape(request.form['id'])
                    specialty = escape(request.form['especialidad'])
                    modalidad = escape(request.form['time'])
                    email = escape(request.form['email'])
                    phonenumber = escape(request.form['phone'])
                    username = escape(request.form['user'])
                    password = escape(request.form['password'])
                    #confirm = escape(request.form['confirm'])
                    role = 2
                    # Validar los datos
                    swerror = False
                    if name == None or len(name) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el nombre del medico', 'advertencia')
                        swerror = True
                    if lastname == None or len(lastname) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el apellido del medico', 'advertencia')
                        swerror = True
                    if tipoid == None or len(tipoid) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el tipo de documento', 'advertencia')
                        swerror = True
                    if id == None or len(id) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
                        swerror = True
                    if specialty == None or len(specialty) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar la especialidad del m??dico', 'advertencia')
                        swerror = True
                    if modalidad == None or len(modalidad) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar la jornada de trabajo del m??dico', 'advertencia')
                        swerror = True
                    if username == None or len(username) == 0 or not login_valido(username):
                        flash(
                            'ADVERTENCIA: Debe suministrar un usuario v??lido', 'advertencia')
                        swerror = True
                    if email == None or len(email) == 0 or not email_valido(email):
                        flash(
                            'ADVERTENCIA: Debe suministrar un email v??lido', 'advertencia')
                        swerror = True
                    if password == None or len(password) == 0 or not pass_valido(password):
                        flash(
                            'ADVERTENCIA: Debe suministrar una clave v??lida', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Preparar la consulta
                        pwd = generate_password_hash(
                            password)  # Cifrar la clave
                        sql = 'INSERT INTO M??dico(nombres,apellidos,tipoId,NumeroId,idespecialidad,modalidad,mail,tel??fono,usuario,clave,idrol) VALUES(?,?,?,?,?,?,?,?,?,?,?)'
                        res = accion(sql, (name, lastname, tipoid, id, specialty,
                                     modalidad, email, phonenumber, username, pwd, role))
                        # Verificar resultados
                        if res == 0:
                            flash('ERROR: No se pudo insertar el registro', 'error')
                        else:
                            flash(
                                'Datos grabados con exito.', 'actualiza')
                    return render_template('forms/dashboard-medico.html', form=form)

                elif request.form.get('updbtn') == 'Actualizar':
                    name = escape(request.form['name'])
                    lastname = escape(request.form['last'])
                    tipoid = escape(request.form['tipoid'])
                    id = escape(request.form['id'])
                    specialty = escape(request.form['especialidad'])
                    modalidad = escape(request.form['time'])
                    email = escape(request.form['email'])
                    phonenumber = escape(request.form['phone'])
                    username = escape(request.form['user'])
                    password = escape(request.form['password'])
                    #confirm = escape(request.form['confirm'])
                    role = 2
                    # Validar los datos
                    swerror = False
                    if name == None or len(name) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el nombre del medico', 'advertencia')
                        swerror = True
                    if lastname == None or len(lastname) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el apellido del medico', 'advertencia')
                        swerror = True
                    if tipoid == None or len(tipoid) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el tipo de documento', 'advertencia')
                        swerror = True
                    if id == None or len(id) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
                        swerror = True
                    if specialty == None or len(specialty) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar la especialidad del m??dico', 'advertencia')
                        swerror = True
                    if modalidad == None or len(modalidad) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar la jornada de trabajo del m??dico', 'advertencia')
                        swerror = True
                    if password == None or len(password) == 0 or not pass_valido(password):
                        flash(
                            'ADVERTENCIA: Debe suministrar una clave v??lida', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Preparar la consulta
                        pwd = generate_password_hash(
                            password)  # Cifrar la clave
                        sql2 = f"UPDATE M??dico set nombres = ?,apellidos = ?, tipoId = ?,NumeroId=?,idespecialidad=?,modalidad=?,mail=?,tel??fono=?,usuario=?,clave=?,idrol=?  where idmedico = ?"
                        # Ejecutar la consulta
                        res2 = accion(sql2, (name, lastname, tipoid, id, specialty, modalidad,
                                      email, phonenumber, username, pwd, role, session['idmed']))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudieron almacenar los datos, reintente', 'error')
                        else:
                            flash(
                                'Los datos fueron actualizados satisfactoriamente', 'actualiza')
                    return render_template('forms/dashboard-medico.html', form=form)

                elif request.form.get('srchbtn') == 'Buscar':
                    tipoid = escape(request.form['tipoid'])
                    txtNroDoc = escape(request.form['id'])

                    sql = f"SELECT nombres,apellidos,idespecialidad,tel??fono,usuario,mail, clave,modalidad,idmedico,Estado FROM M??dico WHERE tipoId = '{tipoid}' and numeroId = '{txtNroDoc}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    # Proceso los resultados
                    if len(res) != 0:
                        # session.clear()
                        session['tipoid'] = tipoid
                        session['txtNroDoc'] = txtNroDoc
                        session['nombres'] = res[0][0]
                        session['apellidos'] = res[0][1]
                        session['especialidad'] = res[0][2]
                        session['telefono'] = res[0][3]
                        session['usuario'] = res[0][4]
                        session['mail'] = res[0][5]
                        session['modalidad'] = res[0][7]
                        session['idmed'] = res[0][8]
                        Estado = res[0][9]
                        if Estado == "ACTIVO":
                            session['activo'] = True
                        else:
                            session['activo'] = False
                        session['found'] = True
                    else:
                        session['tipoid'] = tipoid
                        session['txtNroDoc'] = txtNroDoc
                        session['nombres'] = ""
                        session['apellidos'] = ""
                        session['especialidad'] = ""
                        session['telefono'] = ""
                        session['usuario'] = ""
                        session['mail'] = ""
                        session['modalidad'] = ""
                        session['found'] = False
                        flash('ERROR: M??dico no existe, debe registrarlo', 'error')
                    return render_template('forms/dashboard-medico.html', form=form)

                elif request.form.get('delbtn') == 'Eliminar':
                    name = escape(request.form['name'])
                    lastname = escape(request.form['last'])
                    tipoid = escape(request.form['tipoid'])
                    id = escape(request.form['id'])
                    specialty = escape(request.form['especialidad'])
                    modalidad = escape(request.form['time'])
                    role = 2
                    # Validar los datos
                    swerror = False
                    if tipoid == None or len(tipoid) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el tipo de documento', 'advertencia')
                        swerror = True
                    if id == None or len(id) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
                        swerror = True
                    if not swerror:
                        sql3 = f"UPDATE M??dico set Estado = ? where idmedico = ?"
                        state = "INACTIVO"
                        # Ejecutar la consulta
                        res2 = accion(sql3, (state, session['idmed']))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudieron Eliminar los datos, reintente', 'error')
                        else:
                            session['activo'] = False
                            flash(
                                'INFO: Los datos fueron eliminados satisfactoriamente', 'info')
                    return render_template('forms/dashboard-medico.html', form=form)

                if request.form.get('recvbtn') == 'Recuperar':
                    tipoid = escape(request.form['tipoid'])
                    id = escape(request.form['id'])
                    specialty = escape(request.form['especialidad'])
                    modalidad = escape(request.form['time'])
                    # Validar los datos
                    swerror = False
                    if tipoid == None or len(tipoid) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el tipo de documento', 'advertencia')
                        swerror = True
                    if id == None or len(id) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
                        swerror = True
                    if specialty == None or len(specialty) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar la especialidad del m??dico', 'advertencia')
                        swerror = True
                    if modalidad == None or len(modalidad) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar la jornada de trabajo del m??dico', 'advertencia')
                        swerror = True
                    if not swerror:
                        sql3 = f"UPDATE M??dico set Estado = ? where idmedico = ?"
                        state = "ACTIVO"
                        # Ejecutar la consulta
                        res2 = accion(sql3, (state, session['idmed']))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo eliminar los datos, reintente', 'error')
                        else:
                            session['activo'] = True
                            flash(
                                'Los datos fueron recuperados satisfactoriamente', 'actualiza')
                return render_template('forms/dashboard-medico.html', form=form)
        else:
            return render_template('pages/invalid.html')
    else:
        return render_template('errors/no_logueado.html')


@app.route('/dashboard/paciente', methods=['GET', 'POST'])
# @login_required
# Con el condicional se aseguran de que la vista se renderiza solo si el usuario est?? logueado
def dashboardpaciente():
    if session:
        if session.get('rol') == '3':
            form = DashBoardPaciente(request.form)
            if request.method == 'GET':
                session['tipoid'] = ""
                session['txtNroDoc'] = ""
                session['nombres'] = ""
                session['apellidos'] = ""
                session['telefono'] = ""
                session['usuario'] = ""
                session['mail'] = ""
                session['found'] = False
                return render_template('forms/dashboard-paciente.html', form=form)
            else:
                if request.form.get('regbtn') == 'Crear Registro':
                    name = escape(request.form['TxtNombres'])
                    lastname = escape(request.form['TxtApellidos'])
                    tipoid = escape(request.form['selTipId'])
                    id = escape(request.form['txtNroDoc'])
                    birthday = escape(request.form['DateFecha'])
                    genero = escape(request.form['selSexo'])
                    rhgrup = escape(request.form['selGrupoRh'])
                    email = escape(request.form['mailUsuario'])
                    phonenumber = escape(request.form['TxtNroCel'])
                    username = escape(request.form['txtUsuario'])
                    password = escape(request.form['PwdClave'])
                    role = 2
                    # Validar los datos
                    swerror = False
                    if name == None or len(name) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el nombre del paciente', 'advertencia')
                        swerror = True
                    if tipoid == None or len(tipoid) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el tipo de documento', 'advertencia')
                        swerror = True
                    if id == None or len(id) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
                        swerror = True
                    if username == None or len(username) == 0 or not login_valido(username):
                        flash(
                            'ADVERTENCIA: Debe suministrar un usuario v??lido', 'advertencia')
                        swerror = True
                    if email == None or len(email) == 0 or not email_valido(email):
                        flash(
                            'ADVERTENCIA: Debe suministrar un email v??lido', 'advertencia')
                        swerror = True
                    if password == None or len(password) == 0 or not pass_valido(password):
                        flash(
                            'ADVERTENCIA: Debe suministrar una clave v??lida', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Preparar la consulta
                        pwd = generate_password_hash(
                            password)  # Cifrar la clave
                        sql = 'INSERT INTO Paciente(nombres,apellidos,tipoId,NumeroId,fechaNacimiento,sexo,grupoSanguineo,mail,telefono,usuario,clave,idrol) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'
                        res = accion(sql, (name, lastname, tipoid, id, birthday,
                                     genero, rhgrup, email, phonenumber, username, pwd, role))
                        # Verificar resultados
                        if res == 0:
                            flash('ERROR: No se pudo insertar el registro', 'error')
                        else:
                            flash(
                                'Datos grabados con exito.', 'actualiza')
                    return render_template('forms/dashboard-paciente.html', form=form)

                if request.form.get('updbtn') == 'Actualizar':
                    name = escape(request.form['TxtNombres'])
                    lastname = escape(request.form['TxtApellidos'])
                    tipoid = escape(request.form['selTipId'])
                    id = escape(request.form['txtNroDoc'])
                    birthday = escape(request.form['DateFecha'])
                    genero = escape(request.form['selSexo'])
                    rhgrup = escape(request.form['selGrupoRh'])
                    email = escape(request.form['mailUsuario'])
                    phonenumber = escape(request.form['TxtNroCel'])
                    username = escape(request.form['txtUsuario'])
                    password = escape(request.form['PwdClave'])
                    role = 1
                    # Validar los datos
                    swerror = False
                    if name == None or len(name) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el nombre del paciente', 'advertencia')
                        swerror = True
                    if tipoid == None or len(tipoid) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el tipo de documento', 'advertencia')
                        swerror = True
                    if id == None or len(id) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
                        swerror = True
                    if password == None or len(password) == 0 or not pass_valido(password):
                        flash(
                            'ADVERTENCIA: Debe suministrar una clave v??lida', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Preparar la consulta
                        sql2 = f"UPDATE Paciente set nombres=?,apellidos=?,tipoId=?,NumeroId=?,fechaNacimiento=?,sexo=?,grupoSanguineo = ?,mail=?,telefono=?,usuario=?,idrol=?  where idpaciente = ?"
                        # Ejecutar la consulta
                        res2 = accion(sql2, (name, lastname, tipoid, id, birthday, genero,
                                      rhgrup, email, phonenumber, username, role, session['idpac']))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            flash(
                                'Los datos fueron actualizados satisfactoriamente', 'actualiza')
                    return render_template('forms/dashboard-paciente.html', form=form)

                if request.form.get('srchbtn') == 'Buscar':
                    tipoid = escape(request.form['selTipId'])
                    txtNroDoc = escape(request.form['txtNroDoc'])

                    sql = f"SELECT nombres,apellidos,fechaNacimiento,sexo,grupoSanguineo,mail,telefono,usuario,clave,idpaciente,Estado FROM Paciente WHERE tipoId = '{tipoid}' and numeroId = '{txtNroDoc}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    # Proceso los resultados
                    if len(res) != 0:
                        # session.clear()
                        session['tipoid'] = tipoid
                        session['txtNroDoc'] = txtNroDoc
                        session['nombres'] = res[0][0]
                        session['apellidos'] = res[0][1]
                        session['DateFecha'] = res[0][2]
                        session['selSexo'] = res[0][3]
                        session['selGrupoRh'] = res[0][4]
                        session['mail'] = res[0][5]
                        session['telefono'] = res[0][6]
                        session['usuario'] = res[0][7]
                        session['clave'] = res[0][8]
                        session['idpac'] = res[0][9]
                        Estado = res[0][10]
                        if Estado == "ACTIVO":
                            session['activo'] = True
                        else:
                            session['activo'] = False
                        session['found'] = True
                    else:
                        session['tipoid'] = tipoid
                        session['txtNroDoc'] = txtNroDoc
                        session['nombres'] = ""
                        session['apellidos'] = ""
                        session['DateFecha'] = ""
                        session['selSexo'] = ""
                        session['selGrupoRh'] = ""
                        session['mail'] = ""
                        session['telefono'] = ""
                        session['usuario'] = ""
                        session['clave'] = ""
                        session['found'] = False
                        flash('ERROR: Paciente no existe, debe registrarlo', 'error')
                    return render_template('forms/dashboard-paciente.html', form=form)

                if request.form.get('delbtn') == 'Eliminar':
                    name = escape(request.form['TxtNombres'])
                    lastname = escape(request.form['TxtApellidos'])
                    tipoid = escape(request.form['selTipId'])
                    id = escape(request.form['txtNroDoc'])
                    role = 1
                    # Validar los datos
                    swerror = False
                    if tipoid == None or len(tipoid) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el tipo de documento', 'advertencia')
                        swerror = True
                    if id == None or len(id) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
                        swerror = True
                    if not swerror:
                        sql3 = f"UPDATE Paciente set Estado = ? where idpaciente = ?"
                        state = "INACTIVO"
                        # Ejecutar la consulta
                        res2 = accion(sql3, (state, session['idpac']))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo eliminar los datos, reintente', 'error')
                        else:
                            session['activo'] = False
                            flash(
                                'INFO: Los datos fueron eliminados satisfactoriamente', 'info')
                    return render_template('forms/dashboard-paciente.html', form=form)

                if request.form.get('recvbtn') == 'Recuperar':
                    tipoid = escape(request.form['selTipId'])
                    id = escape(request.form['txtNroDoc'])
                    # Validar los datos
                    swerror = False
                    if tipoid == None or len(tipoid) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar el tipo de documento', 'advertencia')
                        swerror = True
                    if id == None or len(id) == 0:
                        flash(
                            'ADVERTENCIA: Debe suministrar un numero de identificaci??n', 'advertencia')
                        swerror = True
                    if not swerror:
                        sql3 = f"UPDATE Paciente set Estado = ? where idpaciente = ?"
                        state = "ACTIVO"
                        # Ejecutar la consulta
                        res2 = accion(sql3, (state, session['idpac']))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo eliminar los datos, reintente', 'error')
                        else:
                            session['activo'] = True
                            flash(
                                'Los datos fueron recuperados satisfactoriamente', 'actualiza')
                return render_template('forms/dashboard-paciente.html', form=form)
        else:
            return render_template('pages/invalid.html')
    else:
        return render_template('errors/no_logueado.html')


@app.route('/citasForm', methods=['GET', 'POST'])
# Con el condicional se aseguran de que la vista se renderiza solo si el usuario est?? logueado
def citas():
    if request.method == 'GET':
        form = CitaForm(request.form)
        # Preparar la consulta
        sqlpac = f"SELECT NumeroId FROM Paciente WHERE usuario = '{session['usr']}'"
        # Ejecutar la consulta
        respac = seleccion(sqlpac)
        return render_template('forms/citasForm.html', form=form, idp=respac[0][0])
    elif request.method == 'POST':
        # Recuperar los datos del formulario
        idp = escape(request.form['id_paciente'])
        especialidad = escape(request.form['especialidad'])
        idm = escape(request.form['idm'])
        hora = escape(request.form['time'])
        fecha = escape(request.form['fecha'])
        comentario = ""
        valoracion = ""
        # Preparar la consulta
        # Recuperar Ids de BD
        sqlidmed = f"SELECT idmedico FROM M??dico WHERE numeroId = '{idm}'"
        sqlidpac = f"SELECT idpaciente FROM Paciente WHERE NumeroId = '{idp}'"
        residmed = seleccion(sqlidmed)
        residpac = seleccion(sqlidpac)
        # Preparar la consulta
        sql = "INSERT INTO Cita(idpaciente, especialidad, idmedico, horario, fecha, comentarios, valoracion) VALUES (?,?,?,?,?,?,?)"
        res = accion(sql, (residpac[0][0], especialidad, residmed[0][0],
                     hora, fecha, comentario, valoracion))
        # Verificar resultados
        if res == 0:
            flash('ERROR: No se pudo insertar el registro', 'error')
        else:
            flash('Datos grabados con exito en la base de datos.', 'actualiza')
        return redirect(url_for('lista'))

# rutas del dashboard administrativo


@app.route('/Dashboard-Admin/')
def DashboardAdmin():
    if request.method == 'GET':
        return render_template('forms/DashboardAdmin.html')


# LAS SIGUIENTES 4 RUTAS EST??N COMENTADAS PORQUE YA NO SE USAN
# @app.route('/pacientes/', methods=['GET', 'POST'])
# def pacientes():
#     frm = Paciente()
#     if request.method == 'GET':
#         return render_template('forms/pacientes.html', form=frm)


# @app.route('/vistamedico/', methods=['GET', 'POST'])
# def vistamedico():
#     frm = DashBoardMedico()
#     if request.method == 'GET':
#         return render_template('forms/dashboard-medico.html', form=frm)
#     else:
#         if request.form.get('regbtn') == 'Crear Registro':
#             name = escape(request.form['name'])
#             lastname = escape(request.form['last'])
#             tipoid = escape(request.form['tipoid'])
#             id = escape(request.form['id'])
#             specialty = escape(request.form['especialidad'])
#             modalidad = escape(request.form['time'])
#             email = escape(request.form['email'])
#             phonenumber = escape(request.form['phone'])
#             username = escape(request.form['user'])
#             password = escape(request.form['password'])
#             #confirm = escape(request.form['confirm'])
#             role = 2
#             # Validar los datos
#             swerror = False
#             if name == None or len(name) == 0:
#                 flash('ERROR: Debe suministrar el nombre del medico')
#                 swerror = True
#             if lastname == None or len(lastname) == 0:
#                 flash('ERROR: Debe suministrar el apellido del medico')
#                 swerror = True
#             if tipoid == None or len(tipoid) == 0:
#                 flash('ERROR: Debe suministrar el tipo de documento')
#                 swerror = True
#             if id == None or len(id) == 0:
#                 flash('ERROR: Debe suministrar un numero de identificaci??n')
#                 swerror = True
#             if specialty == None or len(specialty) == 0:
#                 flash('ERROR: Debe suministrar la especialidad del m??dico')
#                 swerror = True
#             if modalidad == None or len(modalidad) == 0:
#                 flash('ERROR: Debe suministrar la jornada de trabajo del m??dico')
#                 swerror = True
#             if username == None or len(username) == 0 or not login_valido(username):
#                 flash('ADVERTENCIA: Debe suministrar un usuario v??lido', 'advertencia')
#                 swerror = True
#             if email == None or len(email) == 0 or not email_valido(email):
#                 flash('ADVERTENCIA: Debe suministrar un email v??lido', 'advertencia')
#                 swerror = True
#             if password == None or len(password) == 0 or not pass_valido(password):
#                 flash('ADVERTENCIA: Debe suministrar una clave v??lida', 'advertencia')
#                 swerror = True
#             # if confirm == None or len(confirm) == 0 or not pass_valido(confirm):
#             #    flash('ADVERTENCIA: Debe suministrar una verificaci??n de clave v??lida', 'advertencia')
#             #    swerror = True
#             # if password != confirm:
#             #    flash('ERROR: La clave y la confirmaci??n no coinciden', 'error')
#             #    swerror = True
#             if not swerror:
#                 # Preparar la consulta
#                 pwd = generate_password_hash(password)  # Cifrar la clave
#                 sql = 'INSERT INTO M??dico(nombres,apellidos,tipoId,NumeroId,idespecialidad,modalidad,mail,tel??fono,usuario,clave,idrol) VALUES(?,?,?,?,?,?,?,?,?,?,?)'
#                 res = accion(sql, (name, lastname, tipoid, id, specialty,
#                              modalidad, email, phonenumber, username, pwd, role))
#                 # Verificar resultados
#                 if res == 0:
#                     flash('ERROR: No se pudo insertar el registro')
#                 else:
#                     flash(
#                         'Atualizaci??n: Datos grabados con exito.')
#         return render_template('forms/dashboard-medico.html', form=frm)


# @app.route('/vistapaciente/', methods=['GET', 'POST'])
# def vistapaciente():
#     frm = DashBoardPaciente()
#     if request.method == 'GET':
#         return render_template('forms/dashboard-medico.html', form=frm)


# @app.route('/vistacitas/', methods=['GET', 'POST'])
# def vistacitas():
#     frm = Cita()
#     if request.method == 'GET':
#         return render_template('forms/dashboard-citas.html', form=frm)

# RUTA V??LIDA SOLO PARA PACIENTES POR EL MOMENTO

@app.route('/perfilpac/', methods=['GET', 'POST'])
def perfilpac():
    if session:
        if session.get('rol') == '1':
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
                if request.form.get('action1') == 'Actualizar correo electr??nico':
                    mailUsuario = escape(request.form['mailUsuario'])
                    # pwd = escape(request.form['pwd'])
                    # Validar los datos
                    swerror = False
                    sql = f"SELECT mail, usuario, clave FROM Paciente WHERE usuario='{usuario}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    if mailUsuario == None or len(mailUsuario) == 0 or not email_valido(mailUsuario):
                        flash(
                            'ADVERTENCIA: Debe suministrar un email v??lido', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Proceso los resultados
                        # Preparar el query -- Param??trico
                        sql2 = f"UPDATE Paciente set mail = ? where usuario = ?"
                        # Ejecutar la consulta
                        # pwd = generate_password_hash(pwd)
                        res2 = accion(sql2, (mailUsuario, usuario))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            flash(
                                'Los datos fueron almacenados satisfactoriamente', 'actualiza')
                elif request.form.get('action2') == 'Actualizar usuario':
                    newusr = escape(request.form['usr'])
                    swerror = False
                    sql = f"SELECT mail, usuario, clave FROM Paciente WHERE usuario='{usuario}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    if newusr == None or len(newusr) == 0 or not login_valido(newusr):
                        flash(
                            'ADVERTENCIA: Debe suministrar un usuario v??lido', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Proceso los resultados
                        # Preparar el query -- Param??trico
                        sql2 = f"UPDATE Paciente set usuario = ? where usuario = ?"
                        # Ejecutar la consulta
                        # pwd = generate_password_hash(pwd)
                        res2 = accion(sql2, (newusr, usuario))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            session['usr'] = newusr
                            flash(
                                'Los datos fueron almacenados satisfactoriamente', 'actualiza')
                elif request.form.get('action3') == 'Actualizar contrase??a':
                    newpwd = escape(request.form['pwd'])
                    confirm = escape(request.form['confirm'])
                    swerror = False
                    sql = f"SELECT mail, usuario, clave FROM Paciente WHERE usuario='{usuario}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    # Validar los datos
                    if newpwd == None or len(newpwd) == 0 or not pass_valido(newpwd):
                        flash(
                            'ADVERTENCIA: Debe suministrar una clave v??lida. Utilice un m??nimo de 8 caracteres combinando n??meros, letras, al menos una may??scula y un caracter especial (.,! " # $ %...)', 'advertencia')
                        swerror = True
                    if confirm == None or len(confirm) == 0 or not pass_valido(confirm):
                        flash(
                            'ADVERTENCIA: Debe suministrar una verificaci??n de clave v??lida', 'advertencia')
                        swerror = True
                    if newpwd != confirm:
                        flash(
                            'ERROR: La clave y la confirmaci??n no coinciden', 'error')
                        swerror = True
                    if not swerror:
                        # Proceso los resultados
                        # Preparar el query -- Param??trico
                        sql2 = f"UPDATE Paciente set clave = ? where usuario = ?"
                        # Ejecutar la consulta
                        pwd = generate_password_hash(newpwd)
                        res2 = accion(sql2, (pwd, usuario))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            flash(
                                'Los datos fueron almacenados satisfactoriamente', 'actualiza')
                return render_template('forms/perfil.html', form=frm, data=res)
        else:
            return render_template('pages/invalid.html')
    else:
        return render_template('errors/no_logueado.html')


@app.route('/perfilmed/', methods=['GET', 'POST'])
def perfilmed():
    if session:
        if session.get('rol') == '2':
            frm = Perfil(request.form)
            usuario = session['usr']
            if request.method == 'GET':
                sql = f"SELECT mail, usuario, clave FROM M??dico WHERE usuario='{usuario}'"
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
                if request.form.get('action1') == 'Actualizar correo electr??nico':
                    mailUsuario = escape(request.form['mailUsuario'])
                    # pwd = escape(request.form['pwd'])
                    # Validar los datos
                    swerror = False
                    sql = f"SELECT mail, usuario, clave FROM M??dico WHERE usuario='{usuario}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    if mailUsuario == None or len(mailUsuario) == 0 or not email_valido(mailUsuario):
                        flash(
                            'ADVERTENCIA: Debe suministrar un email v??lido', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Proceso los resultados
                        # Preparar el query -- Param??trico
                        sql2 = f"UPDATE M??dico set mail = ? where usuario = ?"
                        # Ejecutar la consulta
                        # pwd = generate_password_hash(pwd)
                        res2 = accion(sql2, (mailUsuario, usuario))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            flash(
                                'Los datos fueron almacenados satisfactoriamente', 'actualiza')
                elif request.form.get('action2') == 'Actualizar usuario':
                    newusr = escape(request.form['usr'])
                    swerror = False
                    sql = f"SELECT mail, usuario, clave FROM M??dico WHERE usuario='{usuario}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    if newusr == None or len(newusr) == 0 or not login_valido(newusr):
                        flash(
                            'ADVERTENCIA: Debe suministrar un usuario v??lido', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Proceso los resultados
                        # Preparar el query -- Param??trico
                        sql2 = f"UPDATE M??dico set usuario = ? where usuario = ?"
                        # Ejecutar la consulta
                        # pwd = generate_password_hash(pwd)
                        res2 = accion(sql2, (newusr, usuario))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            session['usr'] = newusr
                            flash(
                                'Los datos fueron almacenados satisfactoriamente', 'actualiza')
                elif request.form.get('action3') == 'Actualizar contrase??a':
                    newpwd = escape(request.form['pwd'])
                    confirm = escape(request.form['confirm'])
                    swerror = False
                    sql = f"SELECT mail, usuario, clave FROM M??dico WHERE usuario='{usuario}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    # Validar los datos
                    if newpwd == None or len(newpwd) == 0 or not pass_valido(newpwd):
                        flash(
                            'ADVERTENCIA: Debe suministrar una clave v??lida', 'advertencia')
                        swerror = True
                    if confirm == None or len(confirm) == 0 or not pass_valido(confirm):
                        flash(
                            'ADVERTENCIA: Debe suministrar una verificaci??n de clave v??lida', 'advertencia')
                        swerror = True
                    if newpwd != confirm:
                        flash(
                            'ERROR: La clave y la confirmaci??n no coinciden', 'error')
                        swerror = True
                    if not swerror:
                        # Proceso los resultados
                        # Preparar el query -- Param??trico
                        sql2 = f"UPDATE M??dico set clave = ? where usuario = ?"
                        # Ejecutar la consulta
                        pwd = generate_password_hash(newpwd)
                        res2 = accion(sql2, (pwd, usuario))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            flash(
                                'Los datos fueron almacenados satisfactoriamente', 'actualiza')
                return render_template('forms/perfil.html', form=frm, data=res)
        else:
            return render_template('pages/invalid.html')
    else:
        return render_template('errors/no_logueado.html')


@app.route('/perfiladmin/', methods=['GET', 'POST'])
def perfiladmin():
    if session:
        if session.get('rol') == '3':
            frm = Perfil(request.form)
            usuario = session['usr']
            if request.method == 'GET':
                sql = f"SELECT mail, usuario, clave FROM Superusuario WHERE usuario='{usuario}'"
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
                if request.form.get('action1') == 'Actualizar correo electr??nico':
                    mailUsuario = escape(request.form['mailUsuario'])
                    # pwd = escape(request.form['pwd'])
                    # Validar los datos
                    swerror = False
                    sql = f"SELECT mail, usuario, clave FROM Superusuario WHERE usuario='{usuario}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    if mailUsuario == None or len(mailUsuario) == 0 or not email_valido(mailUsuario):
                        flash(
                            'ADVERTENCIA: Debe suministrar un email v??lido', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Proceso los resultados
                        # Preparar el query -- Param??trico
                        sql2 = f"UPDATE Superusuario set mail = ? where usuario = ?"
                        # Ejecutar la consulta
                        # pwd = generate_password_hash(pwd)
                        res2 = accion(sql2, (mailUsuario, usuario))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            flash(
                                'Los datos fueron almacenados satisfactoriamente', 'actualiza')
                elif request.form.get('action2') == 'Actualizar usuario':
                    newusr = escape(request.form['usr'])
                    swerror = False
                    sql = f"SELECT mail, usuario, clave FROM Superusuario WHERE usuario='{usuario}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    if newusr == None or len(newusr) == 0 or not login_valido(newusr):
                        flash(
                            'ADVERTENCIA: Debe suministrar un usuario v??lido', 'advertencia')
                        swerror = True
                    if not swerror:
                        # Proceso los resultados
                        # Preparar el query -- Param??trico
                        sql2 = f"UPDATE Superusuario set usuario = ? where usuario = ?"
                        # Ejecutar la consulta
                        # pwd = generate_password_hash(pwd)
                        res2 = accion(sql2, (newusr, usuario))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            session['usr'] = newusr
                            flash(
                                'Los datos fueron almacenados satisfactoriamente', 'actualiza')
                elif request.form.get('action3') == 'Actualizar contrase??a':
                    newpwd = escape(request.form['pwd'])
                    confirm = escape(request.form['confirm'])
                    swerror = False
                    sql = f"SELECT mail, usuario, clave FROM Superusuario WHERE usuario='{usuario}'"
                    # Ejecutar la consulta
                    res = seleccion(sql)
                    # Validar los datos
                    if newpwd == None or len(newpwd) == 0 or not pass_valido(newpwd):
                        flash(
                            'ADVERTENCIA: Debe suministrar una clave v??lida', 'advertencia')
                        swerror = True
                    if confirm == None or len(confirm) == 0 or not pass_valido(confirm):
                        flash(
                            'ADVERTENCIA: Debe suministrar una verificaci??n de clave v??lida', 'advertencia')
                        swerror = True
                    if newpwd != confirm:
                        flash(
                            'ERROR: La clave y la confirmaci??n no coinciden', 'error')
                        swerror = True
                    if not swerror:
                        # Proceso los resultados
                        # Preparar el query -- Param??trico
                        sql2 = f"UPDATE Superusuario set clave = ? where usuario = ?"
                        # Ejecutar la consulta
                        pwd = generate_password_hash(newpwd)
                        res2 = accion(sql2, (pwd, usuario))
                        if res2 == 0:
                            flash(
                                'ERROR: No se pudo almacenar los datos, reintente', 'error')
                        else:
                            flash(
                                'Los datos fueron almacenados satisfactoriamente', 'actualiza')
                return render_template('forms/perfil.html', form=frm, data=res)
        else:
            return render_template('pages/invalid.html')
    else:
        return render_template('errors/no_logueado.html')


@app.route('/vistaBusquedas/', methods=['GET', 'POST'])
def vistaBusquedas():
    if session:
        if session.get('rol') == '3':
            frm = VistaBusquedas()
            if request.method == 'GET':
                return render_template('forms/vistaBusquedas.html', form=frm)
        else:
            return render_template('pages/invalid.html')
    else:
        return render_template('errors/no_logueado.html')


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
