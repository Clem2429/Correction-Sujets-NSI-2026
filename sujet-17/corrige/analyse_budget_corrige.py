import csv

def lire_mouvements_depuis_csv(nom_fichier_csv):
    mouvements_csv = []
    try:
        with open(nom_fichier_csv, mode='r', newline='', encoding='utf-8') as fichier_csv:
            lecteur_csv = csv.DictReader(fichier_csv)
            for ligne in lecteur_csv:
                ligne['montant'] = float(ligne['montant'])
                ligne['mois'] = int(ligne['mois'])
                mouvements_csv.append(ligne)
        return mouvements_csv
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier_csv}' est introuvable.")
        return []

mouvements_test = [
    {'type': 'recette',  'catégorie': 'cotisations',    'montant': 1200.0, 'mois': 1},
    {'type': 'recette',  'catégorie': 'billetterie',    'montant': 300.0,  'mois': 6},
    {'type': 'dépense',  'catégorie': 'fonctionnement', 'montant': 450.0,  'mois': 6},
    {'type': 'dépense',  'catégorie': 'déplacements',   'montant': 200.0,  'mois': 12},
    {'type': 'dépense',  'catégorie': 'salaires',       'montant': 1500.0, 'mois': 12},
    {'type': 'recette',  'catégorie': 'subventions',    'montant': 800.0,  'mois': 12},
]

# =============================================================================
# QUESTION 1 : total_par_type + tests
# =============================================================================

def total_par_type(mouvements, type_mouvement):
    """Renvoie la somme totale des montants pour le type donné ('recette' ou 'dépense')."""
    total = 0
    for m in mouvements:
        if m['type'] == type_mouvement:
            total += m['montant']
    return total

def test_total():
    # Recettes : 1200 + 300 + 800 = 2300
    assert total_par_type(mouvements_test, 'recette') == 2300.0
    # Dépenses : 450 + 200 + 1500 = 2150
    assert total_par_type(mouvements_test, 'dépense') == 2150.0
    # Type inexistant → 0
    assert total_par_type(mouvements_test, 'inconnu') == 0
    print("test_total : OK")

test_total()

# =============================================================================
# QUESTIONS 2 & 3 : solde_annuel – identification et correction du bug
# =============================================================================

def solde_mensuel(mouvements, mois):
    total_recettes = 0
    total_depenses = 0
    for m in mouvements:
        if m['mois'] == mois:
            if m['type'] == 'recette':
                total_recettes += m['montant']
            else:
                total_depenses += m['montant']
    return total_recettes - total_depenses


def solde_annuel(mouvements):
    """
    CORRECTION : la boucle originale était `range(1, 12)` ce qui n'incluait
    pas le mois 12 (décembre). Il faut `range(1, 13)` pour couvrir les 12 mois.
    """
    total = 0
    for m in range(1, 13):    # CORRECTION : 13 au lieu de 12
        total += solde_mensuel(mouvements, m)
    return total

def test_solde_annuel():
    # Calcul manuel :
    # Mois 1  : recettes=1200, dépenses=0    → +1200
    # Mois 6  : recettes=300,  dépenses=450  → -150
    # Mois 12 : recettes=800,  dépenses=1700 → -900
    # Total   : 1200 - 150 - 900 = 150
    assert solde_annuel(mouvements_test) == 150.0, f"Obtenu : {solde_annuel(mouvements_test)}"
    print("test_solde_annuel : OK")

test_solde_annuel()

# Application sur le fichier complet
mouvements_complets = lire_mouvements_depuis_csv("budget_complet.csv")
if mouvements_complets:
    print(f"Solde annuel (fichier complet) : {solde_annuel(mouvements_complets):.2f} €")
