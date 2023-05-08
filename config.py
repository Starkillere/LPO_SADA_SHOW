# -*- coding:utf-8 -*-

import os

SECRET_KEY = "#ak@3j^7wbw_y32zupc06!$3#u!0fo^oyty4ngp0)e#04-vdi9"

MAIL_USERNAME = "lposada.show@outlook.fr"
MAIL_PASSWORD = "d2_TbC?6Dq_UM2582z6F{db+3ez~R=J_"
MAIL_SERVER =  "smtp-mail.outlook.com"
MAIL_PORT =  587
MAIL_USE_TLS = True
MAIL_USE_SSL = False

ADMINISTRATEUR_PASSWORD = "/6Xnnn_3P//z20rEAkr@kk/r5A%ZXeE@"
ADMINISTRATEUR_EMAIL = "anrezkia531@gmail.com"
ADMINISTRATEUR_NOM = "Ayouba"
ADMINISTRATEUR_PRENOM = "Anrezki"
ADMINISTRATEUR_PSEUDO = "Administrateur"

SOURCE_AUDIO = 'DIR_AUD/'
SOURCE_VIDEO = 'DIR_VID/'
SOURCE_IMAGE = 'DIR_IMG/'

if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URI = os.path.join(basedir, 'database.db')
else:
    DATABASE_URI = os.environ['DATABASE_URL']

appdir = os.path.join(os.path.dirname(__file__), 'ShowApp/static')
if not os.path.exists(os.path.join(appdir, 'DIR_AUD')):
    os.makedirs(os.path.join(appdir, 'DIR_AUD'))

if not os.path.exists(os.path.join(appdir, 'DIR_VID')):
    os.makedirs(os.path.join(appdir, 'DIR_VID'))

if not os.path.exists(os.path.join(appdir, 'DIR_IMG')):
    os.makedirs(os.path.join(appdir, 'DIR_IMG'))



