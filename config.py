# -*- coding:utf-8 -*-

import os

SECRET_KEY = os.getenv("SECRET_KEY")

MAIL_USERNAME = "lposada.show@outlook.fr"
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SERVER =  "smtp-mail.outlook.com"
MAIL_PORT =  587
MAIL_USE_TLS = True
MAIL_USE_SSL = False

ADMINISTRATEUR_PASSWORD = os.getenv("ADMINISTRATEUR_PASSWORD")
ADMINISTRATEUR_EMAIL = "adm.lposadashow@gmail.com"
ADMINISTRATEUR_NOM = "Administrateur"
ADMINISTRATEUR_PRENOM = "Administrateur"
ADMINISTRATEUR_PSEUDO = "Administrateur"

SOURCE_AUDIO = 'DIR_AUD/'
SOURCE_VIDEO = 'DIR_VID/'
SOURCE_IMAGE = 'DIR_IMG/'

SOURCE_CSV = 'DIR_CSV/'

# Database initialization
if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

appdir = os.path.join(os.path.dirname(__file__), 'ShowApp/static')
if not os.path.exists(os.path.join(appdir, 'DIR_AUD')):
    os.makedirs(os.path.join(appdir, 'DIR_AUD'))

if not os.path.exists(os.path.join(appdir, 'DIR_VID')):
    os.makedirs(os.path.join(appdir, 'DIR_VID'))

if not os.path.exists(os.path.join(appdir, 'DIR_IMG')):
    os.makedirs(os.path.join(appdir, 'DIR_IMG'))

if not os.path.exists(os.path.join(appdir, 'DIR_CSV')):
    os.makedirs(os.path.join(appdir, 'DIR_CSV'))