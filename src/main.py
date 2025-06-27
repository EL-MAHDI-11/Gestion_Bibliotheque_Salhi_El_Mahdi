from bibliotheque import*
from exceptions import*
from visualisations import*
######################################################################

def afficher_menu():
    print("\n=== MENU BIBLIOTHÈQUE ===")
    print("1. Ajouter un livre")
    print("2. Inscrire un membre")
    print("3. Emprunter un livre")
    print("4. Rendre un livre")
    print("5. Lister tous les livres")
    print("6. Afficher les statistique")
    print("7. Sauvegarder et quitter")

def ID_to_membre(bib, ID):
    for m in bib.membres:
        if m.ID == ID:
            return m
    raise MembreInexistantError()

def ISBN_to_livre(bib, ISBN):
    for l in bib.livres:
        if l.ISBN == ISBN:
            return l
    raise LivreInexistantError()

############################################################################

bib = Bibliotheque()
bib.charger()
while True:
    afficher_menu()
    choix = int(input("choisir un numero : "))
    try:
        match choix:

            case 1:
                ISBN = int(input("ISBN : "))
                titre = input("Titre : ")
                auteur = input("Auteur : ")
                annee = int(input("Année : "))
                genre = input("Genre : ")
                bib.Ajouter(ISBN, titre, auteur, annee, genre)

            case 2:
                nom = input("Nom du membre : ")
                bib.Enregistrer(nom)

            case 3:
                ID = int(input("ID du membre : "))
                ISBN = int(input("ISBN du livre : "))
                membre = ID_to_membre(bib, ID)
                livre = ISBN_to_livre(bib, ISBN)
                bib.Emprunter(membre, livre)
                print("Livre emprunte.")

            case 4:
                ID = int(input("ID du membre : "))
                ISBN = int(input("ISBN du livre à retourner : "))
                membre = ID_to_membre(bib, ID)
                livre = ISBN_to_livre(bib, ISBN)
                bib.Retourner(membre, livre)
                print("Livre retourné.")

            case 5:
                print("\n=== Liste des livres ===")
                for l in bib.livres:
                    print(f"{l.ISBN} - {l.titre} ({l.status})")

            case 6:
                diagramme_genres(bib.livres)
                histogramme_auteurs(bib.livres)
                courbe_emprunts()
            case 7:
                bib.sauvegarder()
                print("Les donne sont sauvegardees, session termee.")
                break

            case _:
                print("Choix invalide.")
    except Exception as e:
        print("Erreur :", e)

