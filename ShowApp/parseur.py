#-*- coding:utf-8 -*-

def parseur(title:str, type:str, auteur:str, date:str, text:str, image_font:str, aud:str, vid:str) -> dict:
    parss = {"title":title, "type":type, "auteur":auteur, "date":date, "text":text, "image_font":image_font, "aud":aud, "vid":vid}
    
    return parss
