#-*- coding:utf-8 -*-

import sqlite3

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

def select_by_list_id(ids:list, database:str) -> tuple:
    if len(ids) > 0:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            request =  f"select * from Posts where ID_Post in ({','.join(['?']*len(ids))}) ORDER BY pertinence"
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
        print(categorie)
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

def save_post(database:str, type:str, auteur:str, date:str, title:str, description:str, font_img:str, other_img:str, content:str, tags:str, vue:int, like:int, pertinence:int):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request = "insert into Posts (type, auteur, date, title, description, font_img, other_img, content, tags, vue, like, pertinence) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(request, [(type), (auteur), (date), (title), (description), (font_img), (other_img), (content), (tags), (vue), (like), (pertinence)])

        conn.commit()

        request = "select ID_Post from Posts WHERE title = ?"
        cursor.execute(request, [(title)])

        poste = cursor.fetchone()

    return poste[0]