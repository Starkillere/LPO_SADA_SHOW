# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from . import user, gestion_data, register, poste, search, parseur, text_email
import secrets
from datetime import timedelta
from datetime import datetime
import os

app = Flask(__name__, static_url_path='/static')
app.config.from_object("config")
email = Mail(app)

app.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(days=5)

database = app.config["DATABASE_URI"]
img_link = app.config["SOURCE_IMAGE"]
vid_link = app.config["SOURCE_VIDEO"]
aud_link = app.config["SOURCE_AUDIO"]
csv_link = app.config["SOURCE_CSV"]

if not gestion_data.initialisation(database, app.config["ADMINISTRATEUR_PSEUDO"]):
    register.s_inscrire(app.config["ADMINISTRATEUR_PASSWORD"], app.config["ADMINISTRATEUR_EMAIL"], app.config["ADMINISTRATEUR_NOM"], app.config["ADMINISTRATEUR_PRENOM"], app.config["ADMINISTRATEUR_PSEUDO"], 4, database)

@app.route('/')
def acceuil():
    """import sqlite3
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        requel = "delete from Posts"
        cursor.execute(requel)
        db.commit()"""
    posts = gestion_data.return_postes_all(database)
    correct_posts = [parseur.parseur(post[4], post[1], post[2], post[3], post[5], post[6], post[7], post[12]) for post in posts]
    if "CONNECTED" in session:
        return render_template("accueil.html", connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]], posts=correct_posts)
    return render_template("accueil.html", connected=False, posts=correct_posts, wrRole=[user.User.ROLE[4], user.User.ROLE[2]])

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
                test_email = Message("Bienvenue sur LPO SADA SHOW", sender=app.config["MAIL_USERNAME"], recipients=[Email])
                test_email.html = text_email.welcome_text.replace("<urlforlogo>", url_for('static', filename='images/LPO_SADA SHOW_CADRE_NOIR.png')).replace("<username>", session["PSEUDO"]).replace('<urlforinstagram>', "https://instagram.com/lpo.sadashow?igshid=ZGUzMzM3NWJiOQ==").replace('<urlforinstagramlogo>', url_for('static', filename='images/Instagram_icon.webp')).replace('<urlforwebsite>', url_for('acceuil'))
                try:
                    email.send(test_email)
                except:
                    flash("Email invalide !", 'error')
                    return redirect(url_for("delete_user"))
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

@app.route('/rch-or-filter-by/<content>',  methods=["GET", "POST"])
def rch_or_filter_by(content):
    if request.method == "POST":
        if content.startswith("rch"):
            text = request.form["search"]
            posts = gestion_data.select_by_list_id(search.Search(text, database).result, database)
            if posts == False:
                return redirect(url_for("acceuil"))
            correct_posts = [parseur.parseur(post[4], post[1], post[2], post[3], post[5], post[6], post[7], post[12]) for post in posts]
            if "CONNECTED" in session:
                return render_template("accueil.html", posts=correct_posts, connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]])
            return render_template("accueil.html", posts=correct_posts, connected=False, wrRole=[user.User.ROLE[4], user.User.ROLE[2]])
    elif request.method == "GET" and content.startswith("filter-by") and content.split("-")[-1] in poste.Postes.TYPE:
        gestion_data.return_postes_categorie_all(content.split("-")[-1], database)
        posts = gestion_data.return_postes_categorie_all(content.split("-")[-1], database)
        correct_posts = [parseur.parseur(post[4], post[1], post[2], post[3], post[5], post[6], post[7], post[12]) for post in posts]
        if "CONNECTED" in session:
            return render_template("accueil.html", posts=correct_posts, connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]])
        return render_template("accueil.html", posts=correct_posts, connected=False, wrRole=[user.User.ROLE[4], user.User.ROLE[2]])
    else:
        return redirect(url_for("acceuil"))
    
@app.route("/post", methods=["POST"])
def poster():
    if user.User.key(user.User, session["ROLE"]) != 0:
        if request.method == "POST":

            title = request.form["title"]
            type = request.form["type"]
            text = request.form["text"]
            tags = request.form["tags"]

            save_name = secure_filename(title.replace(" ", "-"))

            if type == "article" or type == "podcast":
                img_ex = request.files["image"].filename.split(".")[-1]
                img_font = request.files["image"]
                path_img = save_name+"."+img_ex
                img_font_path = os.path.join((f"ShowApp/static/{img_link}"), path_img)
                if not os.path.exists(img_font_path) and img_ex != '':
                    img_font.save(img_font_path)
                img_font_path = f"{img_link}/{path_img}"
            
            if type == "podcast":
                podcast = request.files["podcast"]
                podcast_ex = podcast.filename.split(".")[-1]
                path_podcast = save_name+"."+podcast_ex
                podcast_font_path = os.path.join(f"ShowApp/static/{aud_link}", path_podcast)
                if not os.path.exists(podcast_font_path) and (img_ex != '' and podcast_ex != '') :
                    podcast.save(podcast_font_path)
                podcast_font_path = f"{aud_link}/{path_podcast}"

            elif type == "interview":
                video = request.files["interview"]
                video_ex = video.filename.split(".")[-1]
                path_video = save_name+"."+video_ex
                video_font_path = os.path.join(f"ShowApp/static/{vid_link}", path_video)
                if not os.path.exists(video_font_path) and video_ex != '':
                    video.save(video_font_path)
                pth_video = f"{vid_link}/{path_video}"
            
            if type == "article":
                gestion_data.save_post(database, {"type":type, "auteur":session["PSEUDO"], "date":str(datetime.now()), "title":title, "description":text, "img":img_font_path, "tags":tags})
            elif type == "podcast":
                gestion_data.save_post(database, {"type":type, "auteur":session["PSEUDO"], "date":str(datetime.now()), "title":title, "description":text, "img":img_font_path, "tags":tags, "aud":podcast_font_path})
            elif type == "interview":
                gestion_data.save_post(database, {"type":type, "auteur":session["PSEUDO"], "date":str(datetime.now()), "title":title, "description":text, "vid":pth_video, "tags":tags})
    return redirect(url_for("acceuil"))

@app.route("/mot-de-passe-oublier", methods=['GET', 'POST'])
def mot_de_passe_oublier():
    if request.method  == "POST":
        Email = request.form["email"]
        if gestion_data.return_user(Email, database) != None:
            new_password = secrets.token_urlsafe(20)
            test_email = Message("LPO SADA SHOW : Mot de passe oublier !", sender=app.config["MAIL_USERNAME"], recipients=[Email])
            test_email.html = text_email.change_password_text.replace("<urlforlogo>", url_for('static', filename='images/LPO_SADA SHOW_CADRE_NOIR.png')).replace("<username>", Email).replace('<password>', new_password)
            try:
                email.send(test_email)
            except:
                flash("Email invalide !", 'error')
                return redirect(request.url)
            register.new_password(new_password, Email, database)
            return redirect(url_for("acceuil"))
        else:
            flash("Votre email n'est pas reconnue !", 'error')
    return render_template("forget_password.html")

@app.route("/profile-kilo/<name>", methods=['GET', 'POST'])
def profile(name):
    if "CONNECTED" in session:
        if request.method == "POST":
            if name == "set-ident":
                gestion_data.update_ident(session["ID"], database, request.form["Email"], request.form["Nom"], request.form["Prenom"])
            elif name == "set-password":
                Email = (gestion_data.return_user_by_id(session["ID"], database))[1]
                ok = register.update_password(request.form["password"], request.form["new-password"], Email, database)
                if not ok:
                    flash("Mot de passe incorrect", 'error')
                    return redirect(request.url)
        return render_template("profile.html", user=gestion_data.return_user_by_id(session["ID"], database), connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]])
    return redirect(url_for("acceuil"))

@app.route("/delete-user", methods=['GET', 'POST'])
def delete_user():
    if "CONNECTED" in session:
        gestion_data.delleteUser(session["ID"], database)
        return redirect(url_for("logout"))
    return redirect(url_for("acceuil"))

@app.route("/admine-shell/<mode>", methods=['GET', 'POST'])
def administrateur(mode):
    if "CONNECTED" in session and session["ROLE"] == user.User.ROLE[4]:
        if request.method == "POST":
            if mode == "add_normal":
                Email = request.form["email"]
                nom = request.form["name"]
                prenom = request.form["surname"]
                pseudo = request.form["in_name"]
                password = secrets.token_urlsafe(24)
                role = request.form["role"]
                creat = register.s_inscrire(password, Email, nom, prenom, pseudo, int(role), database)
                if creat:
                    test_email = Message("Administration LPO SADA SHOW", sender=app.config["MAIL_USERNAME"], recipients=[app.config["ADMINISTRATEUR_EMAIL"]])
                    if int(role) == 4:
                        test_email.html = f"Un compte administrateur viens d'être crée !<br>Nom = {nom}<br>Prenom = {prenom}<br>Pseudo = {pseudo}<br>Email = {Email}"
                    elif int(role) == 2:
                        test_email.html = f"Un compte journaliste viens d'être crée !<br>Nom = {nom}<br>Prenom = {prenom}<br>Pseudo = {pseudo}<br>Email = {Email}"
                    try:
                        email.send(test_email)
                    except:
                        pass

                    test_email = Message("COMPTE LPO SADA SHOW", sender=app.config["MAIL_USERNAME"], recipients=[Email])
                    test_email.html = f"Un compte {user.User.ROLE[int(role)]} viens d'être crée pour vous !<br>Nom : ......... {nom}<br>Prenom : ....... {prenom}<br>Pseudo : ....... {pseudo}</b>Email : ....... {Email}</b>Mot de passe :....... {password}</b>"
                    try:
                        email.send(test_email)
                    except:
                        flash("Email invalide !", 'error')
                        return redirect(url_for("delete_user"))
                    return redirect(url_for("acceuil"))
                else:
                    flash("Pseudo ou Email déjà utilisé !", 'error')
                    return redirect(request.url)
            elif mode == "add_csv":
                csv_files = request.files["csv_file"]
                filename = f'csv-{str(datetime.now())}'+'.'+csv_files.filename.split(".")[-1]
                path_csv = os.path.join((f"ShowApp/static/{csv_link}"), filename)
                csv_files.save(path_csv)
                entete, users =  gestion_data.readcsvfile(path_csv)
                for useri in users:
                    password = secrets.token_urlsafe(24)
                    creat = register.s_inscrire(password, useri[entete[0]], useri[entete[1]], useri[entete[2]], useri[entete[3]], int(useri[entete[4]]), database)
                    if creat:
                        test_email = Message("Administration LPO SADA SHOW", sender=app.config["MAIL_USERNAME"], recipients=[app.config["ADMINISTRATEUR_EMAIL"]])
                        if int(useri[entete[4]]) == 4:
                            test_email.html = f"Un compte administrateur viens d'être crée !<br>Nom = {useri[entete[1]]}<br>Prenom = {useri[entete[2]]}<br>Pseudo = {useri[entete[3]]}<br>Email = {useri[entete[0]]}"
                        elif int(useri[entete[4]]) == 2:
                            test_email.html = f"Un compte journaliste viens d'être crée !<br>Nom = {useri[entete[1]]}<br>Prenom = {useri[entete[2]]}<br>Pseudo = {useri[entete[3]]}<br>Email = {useri[entete[0]]}"
                        try:
                            email.send(test_email)
                        except:
                            pass

                        test_email = Message("COMPTE LPO SADA SHOW", sender=app.config["MAIL_USERNAME"], recipients=[useri[entete[0]]])
                        test_email.html = f"Un compte {user.User.ROLE[int(useri[entete[4]])]} viens d'être crée pour vous !<br>Nom : ......... {useri[entete[1]]}<br>Prenom : ....... {useri[entete[2]]}<br>Pseudo : ....... {useri[entete[3]]}</b>Email : ....... {user[entete[0]]}</b>Mot de passe :....... {password}</b>"
                        try:
                            email.send(test_email)
                        except:
                            pass
            elif mode == "delt_post":
                gestion_data.delletPost(database, request.form["title"], request.form["auteur"], request.form["date"])
            elif mode == "delt_user":
                gestion_data.delleteUser_width_psedo(request.form["pseudo"], database)
        return render_template("administrateur.html")
    return redirect(url_for("acceuil"))

@app.route("/logout")
def logout():
    if "CONNECTED" in session:
        session.pop('CONNECTED', None)
        session.pop('ID', None)
        session.pop("PSEUDO", None)
        session.pop("ROLE", None)
    return redirect(url_for("acceuil"))

@app.errorhandler(404)
def page_not_found(error):
    rror = [{"title":"404 : Tu t'es perdu dans les couloirs !", "type":"article", "auteur":"LPO SADA SHOW", "date":str(datetime.now()), "text":"""Il était une fois une créature mystérieuse qui hantait les couloirs sombres et délabrés du lycée de SADA. On disait qu'elle avait le pouvoir d'enlever les élèves qui s'aventuraient trop loin dans les méandres des couloirs. Les rumeurs disaient que cette créature était en réalité un monstre démoniaque qui se nourrissait de la peur et des cris des élèves. Les plus courageux disaient que le monstre prenait la forme d'un énorme loup noir, mais personne ne sait vraiment ce qu'il est vraiment. Les élèves étaient terrorisés à l'idée de le rencontrer et ils s'enfuyaient à toutes jambes dès qu'ils entendaient un bruit suspect. Beaucoup d'entre eux ont été enlevés par ce monstre, mais jamais personne ne les a retrouvés. Il règne encore aujourd'hui une atmosphère de mystère et de peur au sein du lycée de SADA.""", "image_font":"images/image404.jpg", "aud":None, "vid":None}]
    if "CONNECTED" in session:
        return render_template("accueil.html", connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]], posts=rror)
    return render_template("accueil.html", connected=False, posts=rror, wrRole=[user.User.ROLE[4], user.User.ROLE[2]])

@app.errorhandler(500)
def page_on(error):
    rror = [{"title":"500 : ça ne marche pas  !", "type":"article", "auteur":"LPO SADA SHOW", "date":str(datetime.now()), "text":"""Notre développeur est génial voilà une photo pour vous le prouver (enfin c'est surtout pour nous nous le prouver !)""", "image_font":"images/image505.png", "aud":None, "vid":None}]
    if "CONNECTED" in session:
        return render_template("accueil.html", connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]], posts=rror)
    return render_template("accueil.html", connected=False, posts=rror, wrRole=[user.User.ROLE[4], user.User.ROLE[2]])