#-*- coding:utf-8 -*-

import sqlite3
import csv

def init_db(database):
    with sqlite3.connect(database) as conn:
        cursor =  conn.cursor()
        requete = """CREATE TABLE IF NOT EXISTS "Posts" (
                	"ID_Post"	INTEGER NOT NULL UNIQUE,
                	"type"	TEXT NOT NULL,
                	"auteur"	TEXT NOT NULL,
                	"date"	TEXT NOT NULL,
                	"title"	TEXT NOT NULL,
                	"description"	TEXT NOT NULL,
                	"img"	TEXT,
                	"aud"	TEXT,
                	"tags"	TEXT NOT NULL,
                	"vue"	INTEGER,
                	"like"	INTEGER,
                	"pertinence"	INTEGER,
                	"vid"	TEXT,
                	PRIMARY KEY("ID_Post" AUTOINCREMENT)
                );"""
        
        cursor.execute(requete)

        request = """CREATE TABLE IF NOT EXISTS "Users" (
                	"ID_user"	INTEGER NOT NULL UNIQUE,
                	"Email"	TEXT NOT NULL UNIQUE,
                	"Nom"	TEXT NOT NULL,
                	"Prenom"	TEXT NOT NULL,
                	"Pseudo"	TEXT NOT NULL UNIQUE,
                	"Password"	TEXT NOT NULL,
                	"Role"	INTEGER NOT NULL,
                	"Date"	TEXT NOT NULL,
                	PRIMARY KEY("ID_user" AUTOINCREMENT)
                );"""
        
        cursor.execute(request)

        conn.commit()

        
def initialisation(database, Pseudo:str):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request =  "select * FROM Users WHERE Pseudo = ?"
        cursor.execute(request, [(Pseudo)])

        admin = cursor.fetchone()

        if admin == None:
            return False
    return True

def return_the_new(database:str):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request =  f"SELECT * FROM Posts ORDER BY ID_Post DESC LIMIT 1"
        cursor.execute(request)
        posts = cursor.fetchone()
    
    return posts

def return_user(Email:str, databse:str) -> tuple:
    with sqlite3.connect(databse) as conn:
        cursor = conn.cursor()
        request =  "select * FROM Users WHERE Email = ?"
        cursor.execute(request, [(Email)])

        user =  cursor.fetchone()
        
    return user

def return_user_by_id(id:int, database:str) -> tuple:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request =  "select * FROM Users WHERE ID_user = ?"
        cursor.execute(request, [(id)])

        user =  cursor.fetchone()
        
    return user

def select_by_list_id(ids:list, database:str) -> tuple:
    if len(ids) > 0:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            request =  f"select * from Posts where ID_Post in ({','.join(['?']*len(ids))}) ORDER BY pertinence, ID_Post DESC"
            print(ids)
            cursor.execute(request, ids)

            posts = cursor.fetchall()

        return posts
    return False

def return_postes_all(databse:str) -> tuple:
    with sqlite3.connect(databse) as conn:
        cursor = conn.cursor()
        request = "select * from Posts ORDER BY ID_Post DESC"
        cursor.execute(request)

        postes = cursor.fetchall()
    
    return postes

def return_postes_categorie_all(categorie:str, databse:str) -> tuple:
    with sqlite3.connect(databse) as conn:
        cursor = conn.cursor()
        request = "select * from Posts WHERE type = ? ORDER BY ID_Post DESC"
        cursor.execute(request, [(categorie)])
        postes = cursor.fetchall()
    
    return postes

def return_poste(ID:int, databse:str) -> tuple:
    with sqlite3.connect(databse) as conn:
        cursor = conn.cursor()
        request = "select * from Posts WHERE ID_Post = ?"
        cursor.execute(request, [(ID)])

        poste = cursor.fetchone()

    return poste

def save_post(database:str, data:dict):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request = f"insert into Posts ({''.join([ key+',' for key in data.keys()])[:-1]}) values ({','.join(['?']*len(data))})"
        cursor.execute(request, [(dt) for dt in list(data.values())])

        conn.commit()
        
def update_ident(user_id:int, database:str, Email:str, Nom:str, Prenom:str, Pseudo:str) -> None:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request = "UPDATE Users SET Email = ?, Nom = ?, Prenom = ?, Pseudo = ? WHERE ID_user = ?"
        cursor.execute(request, [(Email), (Nom), (Prenom), (Pseudo), (user_id)])

        conn.commit()

def delleteUser(id:int, database:str):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request = "DELETE FROM Users WHERE ID_user = ?"
        cursor.execute(request, [(id)])

        conn.commit()

def delleteUser_width_psedo(pseudo:str, database:str):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request = "DELETE FROM Users WHERE pseudo = ?"
        cursor.execute(request, [(pseudo)])

        conn.commit()

def delletPost(database:str, title:str, auteur:str, date:str):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request = "DELETE FROM Posts WHERE title = ? AND auteur = ? AND date = ?"
        cursor.execute(request, [(title), (auteur), (date)])

        conn.commit()

def readcsvfile(csvfile:str):
    with open(csvfile, 'r', encoding='utf-8') as fichier:
        entete = csv.reader(fichier)[0]
        users = [dict(user) for user in csv.DictReader(fichier)]
        return (entete, users)

