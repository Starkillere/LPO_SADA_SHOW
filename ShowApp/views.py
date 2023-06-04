# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
from . import user, poste, search, parseur, text_email
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from PIL import Image
import hashlib
import secrets
import csv
import os

app = Flask(__name__, static_url_path='/static')
app.config.from_object("config")
email = Mail(app)

app.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(days=5)

img_link = app.config["SOURCE_IMAGE"]
vid_link = app.config["SOURCE_VIDEO"]
aud_link = app.config["SOURCE_AUDIO"]
csv_link = app.config["SOURCE_CSV"]

db = SQLAlchemy(app)

class Posts(db.Model):
    ID_Post = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200), nullable=False)
    auteur = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    img = db.Column(db.String(200))
    aud = db.Column(db.String(200))
    vid = db.Column(db.String(200))
    tags = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, type:str, auteur:str, title:str, description:str, tags:str, img:str=None, aud:str=None, vid:str=None) -> None:
        self.type = type
        self.auteur = auteur
        self.title = title
        self.description = description 
        self.img = img 
        self.aud = aud 
        self.vid = vid 
        self.tags = tags

class Users(db.Model):
    ID_user = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(200), nullable=False)
    Nom = db.Column(db.String(200))
    Prenom = db.Column(db.String(200))
    Pseudo = db.Column(db.String(200), nullable=False, unique=True)
    Password = db.Column(db.String(200))
    Role = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, Email:str,Nom:str,Prenom:str,Pseudo:str,Password:str,Role:int):
        self.Email = Email
        self.Nom = Nom 
        self.Prenom = Prenom 
        self.Pseudo = Pseudo 
        self.Password = Password 
        self.Role = Role

def t_init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Users(app.config["ADMINISTRATEUR_EMAIL"], app.config["ADMINISTRATEUR_NOM"], app.config["ADMINISTRATEUR_PRENOM"], app.config["ADMINISTRATEUR_PSEUDO"], hashlib.sha256( app.config["ADMINISTRATEUR_PASSWORD"].encode()).hexdigest(), 4))
    db.session.commit()

@app.route('/')
def acceuil():
    posts = Posts.query.order_by(Posts.ID_Post.desc()).all()
    correct_posts = [parseur.parseur(post.title, post.type, post.auteur, post.date, post.description, post.img, post.aud, post.vid) for post in posts]
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

            ok_useremail = Users.query.filter_by(Email=Email).first()
            ok_username = Users.query.filter_by(Pseudo=pseudo).first()
            if ok_username == None and ok_useremail == None:
                suser = Users(Email, nom, prenom, pseudo, hashlib.sha256(password.encode()).hexdigest(), 0)
                db.session.add(suser)
                db.session.commit()

                the_user = Users.query.filter_by(Pseudo=pseudo).first()
                session['CONNECTED'] = True
                session['ID'] = the_user.ID_user
                session['PSEUDO'] = the_user.Pseudo
                session['ROLE'] = user.User.ROLE[the_user.Role]
                test_email = Message("Bienvenue sur LPO SADA SHOW", sender=app.config["MAIL_USERNAME"], recipients=[Email])
                test_email.html = text_email.welcome_text.replace("<urlforlogo>", url_for('static', filename='images/LPO_SADA SHOW_CADRE_NOIR.png')).replace("<username>", session["PSEUDO"]).replace('<urlforinstagram>', "https://www.instagram.com/lpo.sadashow/").replace('<urlforinstagramlogo>', url_for('static', filename='images/Instagram_icon.webp')).replace('<urlforwebsite>', url_for('acceuil'))
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
            connect = Users.query.filter_by(Email=Email, Password=hashlib.sha256(password.encode()).hexdigest()).first()
            if connect != None:
                the_user = connect
                session['CONNECTED'] = True
                session['ID'] = the_user.ID_user
                session['PSEUDO'] = the_user.Pseudo
                session['ROLE'] = user.User.ROLE[the_user.Role]
                redirect(url_for("acceuil"))
            else:
                flash("Email ou mot de passe incorrect", 'error')
                return redirect(request.url)
    return redirect(url_for("acceuil"))

@app.route('/rch-or-filter-by/<content>',  methods=["GET", "POST"])
def rch_or_filter_by(content):
    if request.method == "POST":
        if content.startswith("rch"):
            if request.form["search"] != '':
                text = request.form["search"]
            elif request.form["searchm"] != '':
                text = request.form["searchm"]
            else:
                text = request.form["search"]
            posts = []
            result = search.Search(text, Posts).result
            if result == []:
                return redirect(url_for("acceuil"))
            for ght in result:
                posts.append(Posts.query.filter_by(ID_Post=ght).first())
            correct_posts = [parseur.parseur(post.title, post.type, post.auteur, post.date, post.description, post.img, post.aud, post.vid) for post in posts]
            if "CONNECTED" in session:
                return render_template("accueil.html", posts=correct_posts, connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]])
            return render_template("accueil.html", posts=correct_posts, connected=False, wrRole=[user.User.ROLE[4], user.User.ROLE[2]])
    elif request.method == "GET" and content.startswith("filter-by") and content.split("-")[-1] in poste.Postes.TYPE:
        posts = Posts.query.filter_by(type=content.split("-")[-1]).all()
        correct_posts = [parseur.parseur(post.title, post.type, post.auteur, post.date, post.description, post.img, post.aud, post.vid) for post in posts]
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

            tags = (search.save_on("title", title)+search.save_on("tags", tags))[:-1]

            save_name = secure_filename(title.replace(" ", "-"))

            if type == "article" or type == "podcast":
                img_ex = request.files["image"].filename.split(".")[-1]
                img_font = request.files["image"]
                path_img = save_name+"."+img_ex
                img_font_path = os.path.join((f"ShowApp/static/{img_link}"), path_img)
                exif_img_font_path = os.path.join((f"ShowApp/static/{img_link}"), "exif"+path_img)
                if not os.path.exists(img_font_path) and img_ex != '':
                    img_font.save(exif_img_font_path)
                    image = Image.open(exif_img_font_path)
                    data = list(image.getdata())
                    image_without_exif = Image.new(image.mode, image.size)
                    image_without_exif.putdata(data)
                    image_without_exif.save(img_font_path)
                    image_without_exif.close()
                    if os.path.exists(exif_img_font_path):
                        os.remove(exif_img_font_path)

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
                db.session.add(Posts(type, session["PSEUDO"], title, text, tags, img_font_path))
                db.session.commit()
            elif type == "podcast":
                db.session.add(Posts(type,session["PSEUDO"], title, text, tags, img_font_path, podcast_font_path))
                db.session.commit()
            elif type == "interview":
                db.session.add(Posts(type,session["PSEUDO"], title, text, tags, vid=pth_video))
                db.session.commit() 
    return redirect(url_for("acceuil"))

@app.route("/mot-de-passe-oublier", methods=['GET', 'POST'])
def mot_de_passe_oublier():
    if request.method  == "POST":
        Email = request.form["email"]
        if Users.query.filter_by(Email=Email).first() != None:
            new_password = secrets.token_urlsafe(20)
            test_email = Message("LPO SADA SHOW : Mot de passe oublier !", sender=app.config["MAIL_USERNAME"], recipients=[Email])
            test_email.html = text_email.change_password_text.replace("<urlforlogo>", url_for('static', filename='images/LPO_SADA SHOW_CADRE_NOIR.png')).replace("<username>", Email).replace('<password>', new_password)
            try:
                email.send(test_email)
            except:
                flash("Email invalide !", 'error')
                return redirect(request.url)
            hash_password = hashlib.sha256(new_password.encode()).hexdigest()
            selctuser = Users.query.filter_by(Email=Email).first()
            user = Users.query.get(selctuser.ID_user)
            user.Password = hash_password
            db.session.commit()
            return redirect(url_for("acceuil"))
        else:
            flash("Votre email n'est pas reconnue !", 'error')
    return render_template("forget_password.html")

@app.route("/profile-kilo/<name>", methods=['GET', 'POST'])
def profile(name):
    if "CONNECTED" in session:
        if request.method == "POST":
            if name == "set-ident":
                puser = Users.query.get(session["ID"])
                puser.Nom = request.form["Nom"]
                puser.Prenom = request.form["Prenom"]

                pseudo = request.form["Pseudo"]
                 
                if Users.query.filter_by(Pseudo=pseudo).first() == None or pseudo == session["PSEUDO"]:
                    puser.Pseudo = pseudo
                else:
                    flash("Pseudo déjà utilisé !", 'error')
                
                email = request.form["Email"]

                if Users.query.filter_by(Email=email).first() == None or email == (Users.query.filter_by(ID_user=session["ID"]).first()).Email:
                    puser.Email = email
                else:
                    flash("Email déjà utilisé !", 'error')

                db.session.commit()
            elif name == "set-password":
                ok_user = Users.query.filter_by(ID_user=session["ID"]).first()
                puser = Users.query.get(session["ID"])
                if ok_user.Password == hashlib.sha256(request.form["password"].encode()).hexdigest():
                    hash_password = hashlib.sha256(request.form["new-password"].encode()).hexdigest()
                    puser.Password = hash_password
                    db.session.commit()
                else:
                    flash("Mot de passe incorrect", 'error')
                    return redirect(request.url)
        return render_template("profile.html", user=Users.query.filter_by(ID_user=session["ID"]).first(), connected=session['CONNECTED'], pseudo=session['PSEUDO'], role=session["ROLE"], wrRole=[user.User.ROLE[4], user.User.ROLE[2]])
    return redirect(url_for("acceuil"))

@app.route("/delete-user", methods=['GET', 'POST'])
def delete_user():
    if "CONNECTED" in session:
        user = Users.query.get(session["ID"])
        db.session.delete(user)
        db.session.commit()
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

                ok_useremail = Users.query.filter_by(Email=Email).first()
                ok_username = Users.query.filter_by(Pseudo=pseudo).first()

                if ok_username == None and ok_useremail == None:

                    suser = Users(Email, nom, prenom, pseudo, hashlib.sha256(password.encode()).hexdigest(), int(role))
                    db.session.add(suser)
                    db.session.commit()

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
                    test_email.html = f"Un compte {user.User.ROLE[int(role)]} viens d'être crée pour vous !<br>Nom : ......... {nom}<br>Prenom : ....... {prenom}<br>Pseudo : ....... {pseudo}<br>Email : ....... {Email}<br>Mot de passe :....... {password}<br>"
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
                with open(path_csv, 'r', encoding='utf-8') as fichier:
                    entete = csv.reader(fichier)[0]
                    users = [dict(usera) for usera in csv.DictReader(fichier)]
                for useri in users:
                    password = secrets.token_urlsafe(24)

                    ok_useremail = Users.query.filter_by(Email=useri[entete[0]]).first()
                    ok_username = Users.query.filter_by(Pseudo=pseudo).first()

                    if ok_username == None and ok_useremail == None:
                        suser = Users(useri[entete[0]], useri[entete[1]], useri[entete[2]], useri[entete[3]], hashlib.sha256(password.encode()).hexdigest(), int(useri[entete[4]]))
                        db.session.add(suser)
                        db.session.commit()

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
                        test_email.html = f"Un compte {user.User.ROLE[int(useri[entete[4]])]} viens d'être crée pour vous !<br>Nom : ......... {useri[entete[1]]}<br>Prenom : ....... {useri[entete[2]]}<br>Pseudo : ....... {useri[entete[3]]}<br>Email : ....... {user[entete[0]]}<br>Mot de passe :....... {password}<br>"
                        try:
                            email.send(test_email)
                        except:
                            pass
                os.remove(path_csv)
            elif mode == "delt_post":
                ok_post = Posts.query.filter_by(title=request.form["title"], auteur=request.form["auteur"], date=request.form["date"]).first()
                post = Posts.query.get(ok_post.ID_Post)
                db.session.delete(post)
                db.session.commit()
            elif mode == "delt_user":
                ok_user = Users.query.filter_by(Pseudo=request.form["pseudo"]).first()
                puser = Users.query.get(ok_user.ID_user)
                db.session.delete(puser)
                db.session.commit()
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