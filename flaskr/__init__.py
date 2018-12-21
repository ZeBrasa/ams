import os
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime, date
from random import randint, random
import time
import sqlite3
import json


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
        # try:
            # database = db.get_db()
            # data = database.execute('SELECT * FROM userData WHERE username=?;', (session['username'], )).fetchone()
            # print('data:      ', list(data))
        # except:
            # print('noob')
            
        if request.method == 'POST':
            date = datetime.now()
            date = date.replace(month=randint(datetime.now().timetuple()[1],12), day=randint(datetime.now().timetuple()[2],30), hour=randint(0,23), minute=randint(0,1)*30 )
            limite = 100
            tipoE = "Corrida"
            database = db.get_db()
            database.execute('INSERT INTO eventsdata(tipo_evento, limite, timest,latitude,longitude) VALUES (?,?,?,?,?);', (tipoE, limite, date, str(random()*180-float(90)), str(random()*360-float(180)),))
            database.commit()
            #request.form listen's to name(on input)<input .... name="..">
            if 'Home' in request.form:
                return redirect(url_for('index'))
            elif 'Login' in request.form:
                return redirect(url_for('login'))
            elif 'Events' in request.form:
                return redirect(url_for('events'))
            elif 'Profile' in request.form:
                return redirect(url_for('profile'))
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
            
    @app.route('/events', methods=['GET', 'POST'])
    def events():
        if request.method == 'POST':
            #request.form listens to name(on input)<input .... name="..">
            if 'Home' in request.form:
                return redirect(url_for('index'))
            elif 'Login' in request.form:
                return redirect(url_for('login'))
            elif 'Events' in request.form:
                return redirect(url_for('events'))
            elif 'MyProfile' in request.form:
                return redirect(url_for('profile'))
            elif 'Register' in request.form:
                return redirect(url_for('register'))
            elif 'Log Out' in request.form:
                session.pop('username', None)
                session.pop('logged_in', None)
                return render_template('index.html', username=None)
            else:
                #must be input = [0,1,2,,....]
                database = db.get_db()
                data = database.execute('SELECT * FROM userData WHERE username=?;', (session['username'], )).fetchone()
                #print('data:      ', list(data))
                #print(data[2])
                #print('--', json.loads(data[2]))
                #print('--', list(set(json.loads(data[2]) + [int(list(request.form)[0])])))
                lista = json.dumps(list(set(json.loads(data[2]) + [int(list(request.form)[0])])))
                database.execute('UPDATE userData SET events_joined=? WHERE username=?;', (lista, session['username'], ))
                database.commit()
                print(int(list(request.form)[0]))
                numberParticipantes = database.execute('SELECT * FROM eventsData WHERE id=?;',(int(list(request.form)[0])+1, )).fetchone()[2] - 1
                database.execute('UPDATE eventsData SET limite=? WHERE id=?;', (numberParticipantes, int(list(request.form)[0])+1 , ))
                database.commit()
                
                ##it works
                #print(list(data[int(list(request.form)[0])]))
            
        database = db.get_db()
        data = database.execute('SELECT * FROM eventsData').fetchall()
        return render_template('events.html', get_Events=data)
        
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
                    lista = []
                    database.execute('INSERT INTO userdata VALUES (?,?,?);', (user, generate_password_hash(password), json.dumps(lista),))
                    database.commit()
                    return redirect(url_for('index'))
                #if !database.execute('SELECT username FROM userData IF(username == ?);', (user,)):
                 #   return render_template('register.html', error='User already exists.')
                
                #database.excute('INSERT INTO userData VALUES (?,?);',(user,generate_password_hash(password),))
                else:
                    error = 'User already registered. Please use another user.'
  
        return render_template('register.html', error=error)
     
    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if request.method == 'POST':
            if 'Home' in request.form:
                return redirect(url_for('index'))
            elif 'Login' in request.form:
                return redirect(url_for('login'))
            elif 'Events' in request.form:
                return redirect(url_for('events'))
            elif 'Profile' in request.form:
                return redirect(url_for('profile'))
            elif 'Register' in request.form:
                return redirect(url_for('register'))
            elif 'Log Out' in request.form:
                session.pop('username', None)
                session.pop('logged_in', None)
                return render_template('index.html', username=None)
        
        if 'username' in session:
            database = db.get_db()
            lt = tuple(json.loads(database.execute('SELECT events_joined FROM userData WHERE username=?;',(session['username'],)).fetchone()[0]))
            print(lt)
            lt1 = database.execute('SELECT * FROM eventsData;').fetchall()
            ltFinal = []
            for x in lt1:
                if x[0] in lt:
                    ltFinal.append(list(x))
            print('Final:', ltFinal)
            
        if 'username' in session:
            return render_template('MyProfile.html', username=session['username'], get_Events=ltFinal)
        return render_template('MyProfile.html', username=None)

    @app.route("/cart")
    def cart():
        if 'username' in session:
            database = db.get_db()
            userId  = database.execute('SELECT nome FROM userProfile WHERE username =?;',(session['username'],)).fetchone()[0]
            products = database.execute('SELECT nomeProd, preco FROM products, kart WHERE products.nomeProd = kart.productId AND kart.userId = ' + str(userId)).database.fetchall()
        totalPrice = 0
        for row in products:
            totalPrice += row[2]
        return render_template("cart.html", nomeProd = products, preco=totalPrice)

    @app.route("/addToCart")
    def addToCart():
        if 'email' not in session:
            return redirect(url_for('loginForm'))
        else:
            productId = int(request.args.get('productId'))
            database = db.get_db()
            userId = database.execute('SELECT nome FROM userProfile WHERE =?;',(session['username'],)).fetchone()[0]
            try:
                database.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                database.commit()
                msg = "Added successfully"
            except:
                database.rollback()
                msg = "Error occured"
            database.close()
    @app.route("/checkout", methods=['GET','POST'])
    def payment():
        if 'username' in session:
            database = db.get_db()
            userId  = database.execute('SELECT nome FROM userProfile WHERE username =?;',(session['username'],)).fetchone()[0]
            products = database.execute('SELECT nomeProd, preco FROM products, kart WHERE products.nomeProd = kart.productId AND kart.userId = ' + str(userId)).database.fetchall()
        totalPrice = 0
        for row in products:
            totalPrice += row[2]
            print(row)
            database.execute("INSERT INTO Orders (userId, productId) VALUES (?, ?)", (userId, row[0]))
        database.execute("DELETE FROM kart WHERE userId = " + str(userId))
        database.commit()
        return render_template("checkout.html", products = products, preco=totalPrice)    
    return app