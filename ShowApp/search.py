#-*- coding:utf-8 -*-

from stop_words import get_stop_words
from simplemma import lemmatize, is_known
from spellchecker import SpellChecker

__all__ = ["Search"]

def Import_format_data(table) -> dict:
    Posts = table.query.all()
    dict_Posts = {}
    keys = ["TITLE", "TAGS"]
    for i in range(len(Posts)):
        values = [Posts[i].title, Posts[i].tags]
        dict_Posts[Posts[i].ID_Post] = {k:v for (k,v) in zip(keys, values)}
        
    return dict_Posts

def corecteur_orthographique(mot:str) -> str:
    correcteur_fr =  SpellChecker(language="fr")
    correcteur_fr = correcteur_fr.correction(mot)
    return correcteur_fr

def mots_vide_supprression(text:list[str]) -> list[str]:
    non_vide = [word for word in text if word not in get_stop_words('french')]
    return non_vide


def Lemmatisation(word:str) -> str:
    try:
        if is_known(word, lang='fr'):
            word = lemmatize(word, lang='fr')
        elif is_known(word, lang="en"):
            word = lemmatize(word, lang="en")
    except:
        pass
    return word

class Search:
    def __init__(self, user_research:str, table) -> None:
        self.user_research = [Lemmatisation(mot) for mot in mots_vide_supprression([corecteur_orthographique(i )for i in user_research.split(" ")])]
        self.data = Import_format_data(table)
        self.result = self._start_reaserch()
    
    def __str__(self) -> str:
        return f"Recherche = {self.user_research}"
    
    def __repr__(self) -> str:
        return f"Recherche = {self.user_research}"
    
    def __search_with_title(self) -> list:
        compatible_id = []
        for key,value in self.data.items():
            title = [Lemmatisation(mot) for mot in mots_vide_supprression([corecteur_orthographique(i) for i in value["TITLE"].split(" ")])]
            count = 0
            for i in range(len(self.user_research)):
                if self.user_research[i] in title:
                    count += 1 
            if count >= (abs(len(title)-len(self.user_research))):
                compatible_id.append(key)
        return compatible_id
    
    def __search_with_tags(self) -> list:
        compatible_id = []
        for key,value in self.data.items():
            tags = [Lemmatisation(mot) for mot in mots_vide_supprression([corecteur_orthographique(i) for i in value["TAGS"].split(",")])]
            for i in range(len(self.user_research)):
                if self.user_research[i] in tags:
                    compatible_id.append(key)
        return compatible_id

    def _start_reaserch(self) -> list:
        return self.__search_with_title()+self.__search_with_tags()