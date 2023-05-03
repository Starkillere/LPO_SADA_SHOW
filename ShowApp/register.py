# -*- coding:utf-8 -*-

import hashlib
import sqlite3
from datetime import datetime

def s_inscrire(Password:str, Email:str, Nom:str, Prenom:str, Pseudo:str, Role:int, database:str) -> bool:
    creat = False

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        request = "select * from Users WHERE Email = ? OR Pseudo = ?"
        cursor.execute(request, [(Email), (Pseudo)])
        exist_user = cursor.fetchone()

        if exist_user == None:
            creat = True

            hash_password = hashlib.sha1(Password.encode()).hexdigest()

            request = "insert into Users (Email, Nom, Prenom, Pseudo, Password, Role, Date) values (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(request, [(Email), (Nom), (Prenom), (Pseudo), (hash_password), (Role), (str(datetime.now()))])
            connection.commit()

    return creat

def login(Password:str, Email:str, database:str):
    connect = False

    with sqlite3.connect(database) as connection:
        hash_password = hashlib.sha1(Password.encode()).hexdigest()

        cursor = connection.cursor()
        request = "select * FROM Users   WHERE Email = ? AND Password = ?"
        cursor.execute(request, [(Email),(hash_password)])
        is_user = cursor.fetchone()

        if is_user != None:
            connect = True
    
    return connect

def update_password(password:str, new_password:str, Email:str, database:str) -> bool:
    ok = login(password, Email, database)
    if ok:
        hash_password = hashlib.sha1(new_password.encode()).hexdigest()
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            request = "UPDATE Users SET Password = ? WHERE Email = ?"
            cursor.execute(request, [(hash_password), (Email)])

            conn.commit()
    return ok

