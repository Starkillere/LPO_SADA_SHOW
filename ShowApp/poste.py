# -*- coding:utf-8 -*-

class Postes:
    TYPE = ["article", "podcast", "interview"]
    def __init__(self,ID_Poste:int, type:str, auteur:str, date:str, title:str, description:str, font_img:str, other_img:str, content:str, tags:str, vue:int, like:int, pertinence:int) -> None:
        self.ID_Poste = ID_Poste
        self.type = type
        self.auteur = auteur
        self.date = date
        self.title = title
        self.description = description
        self.font_img = font_img
        self.other_img = other_img
        self.content = content
        self.tags = tags
        self.vue = vue
        self.like = like
        self.pertinence = pertinence

    def correc_tags(self) -> list[int]:
        pass