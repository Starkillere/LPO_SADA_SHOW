#-*- coding:utf-8 -*-

import sqlite3

def return_user(Email:str, databse:str) -> str:
    with sqlite3.connect(databse) as conn:
        cursor = conn.cursor()
        request =  "select * FROM Users WHERE Email = ?"
        cursor.execute(request, [(Email)])

        user =  cursor.fetchone()
        
    return user

def return_search(database:str) -> dict:
    pass

def return_poste_search(id:list, database:str) -> dict:
    pass