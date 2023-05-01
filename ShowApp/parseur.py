#-*- coding:utf-8 -*-

def parseur(content:str, type:str, img_font:str, title:str, description:str, auteur:str, date:str) -> dict:
    parss = {'img_font':img_font, 'title':title, "description":description, "content":content, "type":type, "auteur":auteur, "date":date}
    
    return parss
