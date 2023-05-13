#-*- coding:utf-8 -*-

import sqlite3

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
        