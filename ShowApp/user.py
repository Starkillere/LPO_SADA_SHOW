# -*- coding:utf-8 -*-

class User:

    ROLE = {4:"ADMINISTRATEUR", 2:"CONTRIBUTEUR", 0:"UTILISATEUR"}

    def __init__(self, ID_user:int, Email:str, Nom:str, Prenom:str, Pseudo:str, Role:int, Date) -> None:
        self.ID_user = ID_user
        self.Email = Email
        self.Nom = Nom
        self.Prenom = Prenom
        self.Pseudo = Pseudo
        self.Role = Role
        self.Date =  Date

    def __repr__(self) -> str:
        return "ID : "+str(self.ID_user)+"\n"+"E-mail : "+self.Email+"\n"+"Nom : "+self.Nom+"\n"+"Prénom : "+self.Prenom+"\n"+"Pseudo : "+self.Pseudo+"\n"+"Role : "+self.ROLE[self.Role]+"\n"+"Date d'inscription : "+self.Date

    def __str__(self) -> str:
        return "ID : "+str(self.ID_user)+"\n"+"E-mail : "+self.Email+"\n"+"Nom : "+self.Nom+"\n"+"Prénom : "+self.Prenom+"\n"+"Pseudo : "+self.Pseudo+"\n"+"Role : "+self.ROLE[self.Role]+"\n"+"Date d'inscription : "+self.Date
    
    def str_role(self) -> str:
        return self.ROLE[self.Role]

