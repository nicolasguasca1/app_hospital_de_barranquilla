#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, session, flash
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from markupsafe import escape
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
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


@app.route('/')
@app.route('/index/')
@app.route('/home/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method=='GET':
        return render_template('forms/login.html', form=form)
    else: 
        # Recuperar los datos
        usr = escape(form.usr.data.strip())
        pwd = escape(form.pwd.data.strip( ))
        # Validar los datos
        swvalido = True
        if len(usr)<6 or len(usr)>40:
            swvalido = False
            flash("El nombre de usuario es requerido y tiene entre 6 y 40 caracteres")
        if len(pwd)<6 or len(pwd)>40:
            swvalido = False
            flash("El nombre de usuario es requerido y tiene entre 6 y 40 caracteres")
        # Realizar el login simulado
        if swvalido and usr=='test123' and pwd=='test123':
            session.clear()
            session['usr_id'] = usr
            session['pwd_id'] = pwd
            return render_template('pages/placeholder.home.html')
        else:
            return render_template('forms/login.html', form=form)



@app.route('/registropac')
def registropac():
    pacform = RegisterFormPac(request.form)
    return render_template('forms/registropac.html', form=pacform)

@app.route('/registromed')
def registromed():
    medform = RegisterFormMed(request.form)
    return render_template('forms/registromed.html', form=medform)

@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/lista/')
def lista():
    return render_template('pages/list.html')

@app.route('/vistamedico')
def vistamedic():
    form = MedicForm(request.form)
    return render_template('forms/vistamedico.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
