# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from . import user, gestion_data, register
from datetime import timedelta
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(days=5)
database = app.config["DATABASE_URI"]

@app.route('/')
def acceuil():
    if "CONNECTED" in session:
        return render_template("accueil.html", connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]])
    return render_template("accueil.html", connected=False)

@app.route('/s-inscrire',  methods=["GET", "POST"])
def s_inscrire():
    if not "CONNECTED" in session:
        if request.method == "POST":
            Email = request.form["email"]
            nom = request.form["name"]
            prenom = request.form["surname"]
            pseudo = request.form["in_name"]
            password = request.form["password"]
            creat = register.s_inscrire(password, Email, nom, prenom, pseudo, 0, database)
            if creat:
                the_user = gestion_data.return_user(Email, database)
                the_user = user.User(the_user[0],the_user[1],the_user[2],the_user[3],the_user[4], the_user[6], the_user[7])
                session['CONNECTED'] = True
                session['ID'] = the_user.ID_user
                session['PSEUDO'] = the_user.Pseudo
                session['ROLE'] = the_user.str_role()
                return redirect(url_for("acceuil"))
            else:
                flash("Pseudo ou Email déjà utilisé !", 'error')
                return redirect(request.url)
        return render_template("login_up.html")
    else:
        return redirect(url_for("acceuil"))
    
@app.route('/login',  methods=["GET", "POST"])
def login():
    if not "CONNECTED" in session:
        if request.method == "POST":
            Email = request.form["email"]
            password = request.form["password"]
            connect = register.login(password, Email, database)
            if connect:
                the_user = gestion_data.return_user(Email, database)
                the_user = user.User(the_user[0],the_user[1],the_user[2],the_user[3],the_user[4], the_user[6], the_user[7])
                print(the_user.Role)
                session['CONNECTED'] = True
                session['ID'] = the_user.ID_user
                session['PSEUDO'] = the_user.Pseudo
                session['ROLE'] = the_user.str_role()
                redirect(url_for("acceuil"))
            else:
                flash("Email ou mot de passe incorrect", 'error')
                return redirect(request.url)
    return redirect(url_for("acceuil"))

@app.route('/recherche',  methods=["GET", "POST"])
def recherche():
    if request.method == "POST":
        text = request.form["search"]
        pass

@app.route("/resutlta", methods=["GET", "POST"])
def resulta():
    return render_template("resulta.html")


@app.route("/logout")
def logout():
    if "CONNECTED" in session:
        session.pop('CONNECTED', None)
        session.pop('ID', None)
        session.pop("PSEUDO", None)
        session.pop("ROLE", None)
    return redirect(url_for("acceuil"))

