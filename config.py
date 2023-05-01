# -*- coding:utf-8 -*-

import os

SECRET_KEY = "D3ggg><LlD 5>5L|5LzLo#z\"Z#L57D_<"

appdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ShowApp')
if not os.path.exists(os.path.join(appdir, 'DIR_AUD')):
    os.makedirs(os.path.join(appdir, 'DIR_AUD'))

if not os.path.exists(os.path.join(appdir, 'DIR_VID')):
    os.makedirs(os.path.join(appdir, 'DIR_VID'))

if not os.path.exists(os.path.join(appdir, 'DIR_IMG')):
    os.makedirs(os.path.join(appdir, 'DIR_IMG'))

SOURCE_AUDIO = os.path.join(appdir, 'DIR_AUD')
SOURCE_VIDEO = os.path.join(appdir, 'DIR_VID')
SOURCE_IMAGE = os.path.join(appdir, 'DIR_IMG')

if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URI = os.path.join(basedir, 'database.db')
else:
    DATABASE_URI = os.environ['DATABASE_URL']