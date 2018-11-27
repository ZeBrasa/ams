import os
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import sqlite3


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    @app.route('/', methods=['GET', 'POST'])
    def index(username=None):
        if 'username' in session:
            print(session['username'])
        else:
            print('fuck')
           
        if request.method == 'POST':
            #request.form listens to name(on input)<input .... name="..">
            if 'Login' in request.form:
                return redirect(url_for('login'))
            elif 'Register' in request.form:
                return redirect(url_for('register'))
            elif 'Log Out' in request.form:
                session.pop('username', None)
                session.pop('logged_in', None)
                return render_template('index.html', username=None)
                
        if 'username' in session:
            return render_template('index.html', username=session['username'] )
        else:
            return render_template('index.html', username=None)
        
    # Route for handling the login page logic
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            #getting user and password text
            user = request.form['username']
            password = request.form['password']
            
            database = db.get_db()
            userDB = database.execute('SELECT username FROM userData WHERE username=?;', (user,)).fetchone()
            if userDB == None:
                error = 'There is no user named with ' + user + '.'
            else:
                passwordDB = database.execute('SELECT password FROM userData WHERE username=?;', (user,)).fetchone()
                if check_password_hash(passwordDB[0], password):
                    session['username'] = user
                    session['logged_in'] = True
                    return redirect(url_for('index'))
                else:
                    error = 'Invalid Credentials. Please try again.'
                #print(check_password_hash(passwordDB, password))
                #if check_password_hash(passwordDB, password):
                #    session['username'] = user
                #    session['logged_in'] = True
                
        return render_template('login.html', error=error)
        
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        error = None
        if request.method == 'POST':
            #print(request.form['Button'])
            if 'Not now!' == request.form['Button']:
                return redirect(url_for('index'))
            if 'Register' in request.form['Button']:
                user = request.form['username']
                password = request.form['password']
                repeatedpass = request.form['repeatpassword']
                if password != repeatedpass:
                    return render_template('register.html', error='Password must be correct.')
                    
                #Everything is check with User not in database
                database = db.get_db()
                if database.execute('SELECT username FROM userData WHERE username=?;', (user,)).fetchone() == None:
                    database.execute('INSERT INTO userdata VALUES (?,?);', (user, generate_password_hash(password),))
                    database.commit()
                    return redirect(url_for('index'))
                #if !database.execute('SELECT username FROM userData IF(username == ?);', (user,)):
                 #   return render_template('register.html', error='User already exists.')
                
                #database.excute('INSERT INTO userData VALUES (?,?);',(user,generate_password_hash(password),))
                else:
                    error = 'User already registered. Please use another user.'
  
        return render_template('register.html', error=error)
        
        
    
    return app