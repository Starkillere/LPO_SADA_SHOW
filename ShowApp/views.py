# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from . import user, gestion_data, register, poste, search, parseur
from datetime import timedelta
from datetime import datetime
import os

app = Flask(__name__, static_url_path='/static')
app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(days=5)
database = app.config["DATABASE_URI"]

img_link = app.config["SOURCE_IMAGE"]
vid_link = app.config["SOURCE_VIDEO"]
aud_link = app.config["SOURCE_AUDIO"]

@app.route('/')
def acceuil():
    """import sqlite3
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        requel = "delete from Posts"
        cursor.execute(requel)
        db.commit()"""
    if "CONNECTED" in session:
        return render_template("accueil.html", connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]], new=gestion_data.return_the_new(database))
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
        all_posts = gestion_data.select_by_list_id(search.Search(text, database).result, database)
        return render_template("resulta.html", news=all_posts)
    else:
        return redirect(url_for("acceuil"))

@app.route("/resutlta/<name>", methods=["GET", "POST"])
def resulta(name):
    if request.method == "POST":
        choice =  request.form["item"]
        print(request.form["item"])
        theposte = gestion_data.return_poste(int(choice), database)
        #the_poste = poste.Postes(the_poste[0],the_poste[1],the_poste[2],the_poste[3],the_poste[4],the_poste[5],the_poste[6],the_poste[7],the_poste[8],the_poste[9])
        return render_template("affiche.html", new=parseur.parseur(theposte[8], theposte[1], theposte[6], theposte[4],theposte[5], theposte[2], theposte[3]))
    else:
        if not name in poste.Postes.TYPE:
            postes = gestion_data.return_postes_all(database)
            return render_template("resulta.html", news=postes)
        elif name in poste.Postes.TYPE:
            postes = gestion_data.return_postes_categorie_all(name, database)
            return render_template("resulta.html", news=postes)

@app.route("/print/<name>", methods=["GET", "POST"])
def print(name):
    theposte = gestion_data.return_poste(int(name), database)
    return render_template("affiche.html", new=parseur.parseur(theposte[8], theposte[1], theposte[6], theposte[4],theposte[5], theposte[2], theposte[3]))

@app.route("/post/<name>", methods=["GET","POST"])
def post(name):
    if user.User.key(user.User, session["ROLE"]) != 0:
        if request.method == "POST" and session["ROLE"] != 0:
            img_font = secure_filename(request.files["img_font"].filename)
            img_font_path = os.path.join((f"ShowApp/static/{img_link}"), img_font)
            if not os.path.exists(img_font_path):
                request.files["img_font"].save(img_font_path)
            img_font_path = f"{img_link}/{img_font}"

            title = request.form["title"]
            description = request.form["description"]

            if name == "article":
                article = request.form["article"]
                content = article

            elif name == "podcast":
                podcast = secure_filename(request.files["podcast"].filename)
                podcast_path = os.path.join(f"ShowApp/static/{aud_link}", podcast)
                if not os.path.exists(podcast_path):
                    request.files["podcast"].save(podcast_path)
                content = f"{aud_link}/{podcast}"

            elif name == "interview":
                interview = secure_filename(request.files["interview"].filename)
                interview_path = os.path.join(f"ShowApp/static/{vid_link}", interview)
                if not os.path.exists(interview_path):
                    request.files["interview"].save(interview_path)
                content = f"{vid_link}/{interview}"

            tags = request.form["tags"]
            auteur = session['PSEUDO']
            date = str(datetime.now())

            ID = gestion_data.save_post(database, name, auteur, date, title, description, img_font_path, "none", content, tags, 0, 0, 0)
            theposte = gestion_data.return_poste(int(ID), database)
            return render_template("affiche.html", new=parseur.parseur(theposte[8], theposte[1], theposte[6], theposte[4],theposte[5], theposte[2], theposte[3]))
        if name == "post-choice":
            return render_template("posts.html")
        return render_template("edit_w.html", type=name)
    else:
        return redirect(url_for("acceuil"))

@app.route("/profile/<name>", methods=['GET', 'POST'])
def profile(name):
    if "CONNECTED" in session:
        if request.method == "POST":
            if name == "set-ident":
                gestion_data.update_ident(session["ID"], database, request.form["Email"], request.form["Nom"], request.form["Prenom"], request.form["Pseudo"])
                session["PSEUDO"] = request.form["Pseudo"]
            elif name == "set-password":
                Email = (gestion_data.return_user_by_id(session["ID"], database))[1]
                ok = register.update_password(request.form["password"], request.form["new-password"], Email, database)
                if not ok:
                    flash("Mot de passe incorrect", 'error')
                    return redirect(request.url)
        return render_template("profile.html", user=gestion_data.return_user_by_id(session["ID"], database))
    return redirect(url_for("acceuil"))

@app.route("/delete-user", methods=['GET', 'POST'])
def delete_user():
    if "CONNECTED" in session:
        gestion_data.delleteUser(session["ID"], database)
        return redirect(url_for("logout"))
    return redirect(url_for("acceuil"))  

@app.route("/admine-shell", methods=['GET', 'POST'])
def administrateur():
    if request.method == "GET":
        return render_template("administrateur.html", )

@app.route("/logout")
def logout():
    if "CONNECTED" in session:
        session.pop('CONNECTED', None)
        session.pop('ID', None)
        session.pop("PSEUDO", None)
        session.pop("ROLE", None)
    return redirect(url_for("acceuil"))