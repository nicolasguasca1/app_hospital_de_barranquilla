#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, session, flash, redirect, url_for
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
import sys
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


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if session['usr_id']:
    #     return redirect(url_for('home'))
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('forms/login.html', form=form)
    # elif form.btn():
    #     user = get_user(form.usr.data)
    #     myUser = User(user.id.data,user.name.data,user.usr.data,user.pwd.data,user.isAdmin.data)
    #     if user is not None and myUser.check_password(form.pwd.data):
    #         login_user(user)
    #         next_page = request.args.get('next')
    #         if not next_page or url_parse(next_page) .netloc != '':
    #             next_page = url_for('pages/placeholder.home.html')
    #         return redirect(next_page)
    #     return render_template('forms/login.html', form=form)
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
        sqlmed = f"SELECT idmedico, nombres, mail, clave FROM Médico WHERE usuario = '{usr}'"
        sqlpac = f"SELECT idpaciente, nombres, mail, clave FROM Paciente WHERE usuario = '{usr}'"
        sqladmin = f"SELECT idsuper, nombres, mail, clave FROM Superusuario WHERE usuario = '{usr}'"

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
    # else:


@app.route('/registromed', methods=['GET', 'POST'])
def registromed():
    if request.method == 'GET':
        medform = RegisterFormMed(request.form)
    return render_template('forms/registromed.html', form=medform)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/lista/')
def lista():
    if session:
        return render_template('pages/lista.html')
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


@app.route('/citasForm', methods=['GET', 'POST'])
# Con el condicional se aseguran de que la vista se renderiza solo si el usuario está logueado
def citas():
    if request.method == 'POST':
        form = CitaForm(request.form)
        return render_template('forms/citasForm.html', form=form)

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


@app.route('/perfil/', methods=['GET', 'POST'])
def perfil():
    frm = Perfil()
    if request.method == 'GET':
        return render_template('forms/perfil.html', form=frm)


@app.route('/vistaBusquedas/', methods=['GET', 'POST'])
def vistaBusquedas():
    frm = VistaBusquedas()
    if request.method == 'GET':
        return render_template('forms/vistaBusquedas.html', form=frm)


@app.route('/logout/')
def logout():
    session.clear()
    return redirect('pages/placeholder.home.html')

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
