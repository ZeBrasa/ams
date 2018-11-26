import os
from flask import Flask, render_template, redirect, url_for, request
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


    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            #request.form listens to name(on input)
            if "Login" in request.form:
                return redirect(url_for("login"))
            elif "Register" in request.form:
                return redirect(url_for("register"))
        return render_template("index.html")
        #return render_template('%s.html' % page_name)
        
        
    # Route for handling the login page logic
    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            #getting user and password text
            user = request.form["username"]
            password = request.form["password"]
            
            # db = sqlite3.connect("database.db")
            # cursor= db.cursor()
            # cursor.execute("INSERT INTO userData VALUES (?,?,?,?);",(user,password,"","",))
            # db.commit()
            # cursor.execute("SELECT passwordEncrypt FROM userData WHERE user = ?;",(user,))
            # supostamente apenas uma password(Testing)
            # for row in cursor:
                # print(row[0])
            # cursor.close()
            # db.close()
            
            if user == "admin" or password == "admin":
                #chama a função, não o html
                return redirect(url_for("index"))
            else:
                error = "Invalid Credentials. Please try again."
                
        return render_template("login.html", error=error)
        
    @app.route("/register", methods=["GET", "POST"])
    def register():
        error = None
        if request.method == "POST":
            if "LaterButton" in request.form:
                return redirect(url_for("index"))
            elif "RegisterButton" in request.form:
                user = request.form["username"]
                password = request.form["password"]
                return redirect(url_for("index"))
        return render_template("register.html", error=error)
    
    from . import db
    db.init_app(app)
    
    return app