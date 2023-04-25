# -*- coding:utf-8 -*-

import os

SECRET_KEY = "D3ggg><LlD 5>5L|5LzLo#z\"Z#L57D_<"

if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URI = os.path.join(basedir, 'database.db')
else:
    DATABASE_URI = os.environ['DATABASE_URL']