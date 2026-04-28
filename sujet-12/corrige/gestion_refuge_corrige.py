import csv

class Renard:
    """
    Classe représentant un renard dans le refuge.
    Attributs : identifiant, nom, poids, date_arrivee.
    """
    def __init__(self, identifiant, nom, poids, date_arrivee):
        # Question 1 : constructeur
        self.identifiant = identifiant
        self.nom = nom
        self.poids = poids
        self.date_arrivee = date_arrivee

    def __str__(self):
        # Question 2 : méthode __str__
        return f"Renard ID {self.identifiant} - {self.nom} (Arrivé le {self.date_arrivee})"


class Refuge:
    """
    Classe représentant le refuge contenant la liste des renards.
    """
    def __init__(self, nom, adresse):
        self.nom = nom
        self.adresse = adresse
        self.liste_renards = []

    def recueillir(self, un_renard):
        self.liste_renards.append(un_renard)

    def lister_peu_corpulents(self):
        return [renard for renard in self.liste_renards if renard.poids < 6.0]

    def pourcentage_peu_corpulents(self):
        if len(self.liste_renards) == 0:
            return 0.0
        return len(self.lister_peu_corpulents()) / len(self.liste_renards) * 100

    def importer_donnees(self, nom_fichier):
        """
        VERSION CORRIGEE : conversion explicite de id (int) et poids (float).
        L'erreur originale : id et poids restaient des str, causant des erreurs
        lors des comparaisons numériques (poids < 6.0) et manipulations entières.
        """
        print(f"Tentative d'importation depuis {nom_fichier}...")
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            lignes = csv.DictReader(f, delimiter=';')
            for ligne in lignes:
                renard = Renard(
                    int(ligne['id']),        # CORRECTION : conversion en int
                    ligne['nom'],
                    float(ligne['poids']),   # CORRECTION : conversion en float
                    ligne['date_arrivee']
                )
                self.recueillir(renard)


# ---- Tests ----
# Question 2 : test instanciation
renard1 = Renard(200, "Oscar", 5.1, "2026-01-01")
print(renard1)

# Question 3 : test refuge
refuge = Refuge("SOS Goupil", "1 rue de la Forêt, 75000 Paris")
refuge.importer_donnees("donnees_renards.csv")

# Question 4 : analyse corpulence
peu_corpulents = refuge.lister_peu_corpulents()
total = len(refuge.liste_renards)
nb_peu = len(peu_corpulents)
print(f"\nRenards peu corpulents ({nb_peu}/{total}) :")
for r in peu_corpulents:
    print(f"  {r}")
print(f"Pourcentage peu corpulents : {refuge.pourcentage_peu_corpulents():.1f}%")
