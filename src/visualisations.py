import matplotlib.pyplot as plt
from collections import Counter
import csv
from datetime import datetime, timedelta

##################################################

def diagramme_genres(livres):
    genres = [livre.genre for livre in livres]
    compteur = Counter(genres)

    plt.figure(figsize=(6, 6))
    plt.pie(compteur.values(), labels=compteur.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("Repartition des livres par genre")
    plt.axis('equal')
    plt.show()

def histogramme_auteurs(livres):
    auteurs = [livre.auteur for livre in livres]
    compteur = Counter(auteurs)
    top = compteur.most_common(10)

    noms = [auteur for auteur, _ in top]
    nb = [count for _, count in top]

    plt.figure(figsize=(10, 6))
    plt.bar(noms, nb, color='blue')
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 des auteurs les plus populaires")
    plt.xlabel("Auteur")
    plt.ylabel("Nombre de livres")
    plt.tight_layout()
    plt.show()

def courbe_emprunts(f_csv="historique.csv"):
    dates = []

    with open(f_csv, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            date_str = row[0]
            action = row[3]
            if action == "emprunt":
                date = datetime.fromisoformat(date_str)
                if datetime.now() - date <= timedelta(days=30):
                    dates.append(date.date())

    compteur = Counter(dates)
    dates_tries = sorted(compteur.keys())
    valeurs = [compteur[date] for date in dates_tries]

    plt.figure(figsize=(10, 6))
    plt.plot(dates_tries, valeurs, marker='o')
    plt.title("Activité des emprunts (30 derniers jours)")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'emprunts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()