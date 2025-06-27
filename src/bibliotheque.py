from exceptions import*
import json
import csv
import os 
from datetime import datetime
#################################################################

class Livre:
    def __init__(self,ISBN,titre,auteur,annee,genre,status):
        self._ISBN = ISBN
        self._titre=titre
        self._auteur=auteur
        self._annee=annee
        self._genre=genre
        self._status=status

    #getters & setters

    @property
    def ISBN(self):
        return self._ISBN
    @ISBN.setter
    def ISBN(self,ISBN):
        self._ISBN=ISBN

    @property
    def titre(self):
        return self._titre
    @titre.setter
    def titre(self,titre):
        self._titre=titre

    @property
    def auteur(self):
        return self._auteur
    @auteur.setter
    def auteur(self,auteur):
        self._auteur=auteur

    @property
    def annee(self):
        return self._annee
    @annee.setter
    def annee(self,annee):
        self._annee=annee

    @property
    def genre(self):
        return self._genre
    @genre.setter
    def genre(self,genre):
        self._genre=genre

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self,status):
        self._status=status

    #methodes
    def to_dict(self):
        return{
            "ISBN": self._ISBN,
            "titre": self._titre,
            "auteur": self._auteur,
            "annee": self._annee,
            "genre": self._genre,
            "status": self._status
        }
    @staticmethod
    def from_dict(d):
        return Livre(
            d["ISBN"],d["titre"],d["auteur"],d["annee"],d["genre"],d["status"]
    )


########################################################################

class Membre:
    def __init__(self,NOM,ID=None,livres_empruntes=None):
        self._ID= ID
        self._NOM=NOM
        self.livres_empruntes=livres_empruntes if livres_empruntes else []

    #getters & setters

    @property
    def ID(self):
        return self._ID
    @ID.setter
    def ID(self,ID):
        self._ID=ID

    @property
    def NOM(self):
        return self._NOM
    @NOM.setter
    def NOM(self,NOM):
        self._NOM=NOM

    @property
    def livres_empruntes(self):
        return self._livres_empruntes
    @livres_empruntes.setter

    #methodes

    def livres_empruntes(self,livres_empruntes):
        if all(isinstance(l, Livre) for l in livres_empruntes):
            self._livres_empruntes = livres_empruntes
        else:
            raise LivreInexistantError("les elements doivent etre des livres valides.")

    def ajouter_emprunt(self, livre):
        if isinstance(livre,Livre):
            self._livres_empruntes.append(livre)
        else:
            raise LivreInexistantError("ce livre n'existe pas.")

    def supprimer_emprunt(self, livre):
        if isinstance(livre,Livre):
            self._livres_empruntes.remove(livre)

    def to_dict(self):
        return {
            "ID": self._ID,
            "NOM": self._NOM,
            "livres_empruntes": [livre.ISBN for livre in self._livres_empruntes]
        }

    @staticmethod
    def from_dict(d, livres_disponibles):
        livres = [livre for livre in livres_disponibles if livre.ISBN in d["livres_empruntes"]]
        return Membre(d["ID"], d["NOM"], livres)

########################################################################

class Bibliotheque:
    def __init__(self, livres=None,membres=None):
        self.livres=livres if livres else []
        self.membres=membres if membres else []

    #getters & setters

    @property
    def livres(self):
        return self._livres
    @livres.setter
    def livres(self,livres):
        if all(isinstance(l, Livre) for l in livres):
            self._livres= livres
        else:
            raise #livre inexistant error
       
    @property
    def membres(self):
        return self._membres
    @membres.setter
    def membres(self,membres):
        if all(isinstance(M, Membre) for M in membres):
            self._membres= membres
        else:
            raise #MembreInexistantError

    #methodes

    def Ajouter(self, ISBN, titre, auteur, annee, genre, status=True):
        for l in self._livres:
            if l.ISBN == ISBN:
                print("Livre déjà existant.")
                return
        nouveau_livre = Livre(ISBN, titre, auteur, annee, genre, status)
        self._livres.append(nouveau_livre)
        print(f"Livre '{titre}' ajouté.")

    
    def supprimer(self,livre):
        if isinstance(livre, Livre) :
            if livre in self._livres:
                self._livres.remove(livre)
                print(f"Le livre '{livre.titre}' a été supprimer.")
            else:
                print(f"Le livre '{livre.titre}' n'existe pas dans la bibliotheque.")
        else:
            raise LivreInexistantError("ce livre n'existe pas.")
  
    
    def Enregistrer(self,NOM):
        for n in self._membres:
            if n.NOM == NOM:
                print("membre deja enregistre.")
                return
        membre = Membre(NOM)
        membre.ID = len(self._membres)
        self._membres.append(membre)
        print(f"Nouveau membre '{NOM}' enregistré avec ID {membre.ID}")

   
    def Emprunter(self,membre, livre):
        if livre not in self._livres:
            raise LivreInexistantError()
        
        if membre not in self._membres:
            raise MembreInexistantError()
        
        if livre.status ==False:
            raise LivreIndisponibleError()
        
        livre.status = False
        membre.ajouter_emprunt(livre)
        self.enregistrer_historique(livre.ISBN, membre.ID, "emprunt")


    def Retourner(self,membre,livre):
        if livre not in self._livres:
            raise LivreInexistantError()
        if membre not in self._membres:
            raise MembreInexistantError()
        if livre not in membre._livres_empruntes:
            raise LivreInexistantError("ce livre n'est pas emprunte par ce membre")
        if livre in self.livres and membre in self.membres and livre in membre.livres_empruntes:
            livre.status=True
            membre.supprimer_emprunt(livre)
            self.enregistrer_historique(livre.ISBN, membre.ID, "retour")
        else:
            print(f"Le livre '{livre.titre}' n'existe pas dans la bibliotheque ou '{membre.NOM}' n'est pas un membre .")

    def sauvegarder(self, f_livres="livres.json", f_membres="membres.json"):
        with open(f_livres, "w") as f:
            json.dump([livre.to_dict() for livre in self._livres], f, indent=4)
        with open(f_membres, "w") as f:
            json.dump([m.to_dict() for m in self._membres], f, indent=4)

    def charger(self, f_livres="livres.json", f_membres="membres.json"):
        if os.path.exists(f_livres):
            with open(f_livres, "r") as f:
                livres_data = json.load(f)
                self._livres = [Livre.from_dict(d) for d in livres_data]

        if os.path.exists(f_membres):
            with open(f_membres, "r") as f:
                membres_data = json.load(f)
                self._membres = [Membre.from_dict(d, self._livres) for d in membres_data]

    def enregistrer_historique(self, ISBN, ID_membre, action, file="historique.csv"):
        with open(file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), ISBN, ID_membre, action])
