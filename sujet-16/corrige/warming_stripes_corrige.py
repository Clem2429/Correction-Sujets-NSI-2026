import csv
import matplotlib.pyplot as plt

def charger(nom_fichier):
    donnees = []
    with open(nom_fichier, mode='r', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        for ligne in lecteur:
            donnees.append({"année": int(ligne["Year"]), "écart": float(ligne["Anomaly"])})
    return donnees

datas_temperature = charger("datas.csv")

# =============================================================================
# QUESTION 1 : ecart_temperature + tests
# =============================================================================

def ecart_temperature(datas, annee):
    """Renvoie l'écart de température pour l'année donnée, ou None si absente."""
    for element in datas:
        if element["année"] == annee:
            return element["écart"]
    return None

# Tests via assertions
assert ecart_temperature(datas_temperature, 1851) == -0.15
assert ecart_temperature(datas_temperature, 2020) == 1.01
assert ecart_temperature(datas_temperature, 9999) is None
print("Tests ecart_temperature : OK")

# =============================================================================
# QUESTION 2 : derniere_annee_ecart_negatif
# =============================================================================

def derniere_annee_ecart_negatif(datas):
    annee = max([element["année"] for element in datas])
    ecart = ecart_temperature(datas, annee)
    while ecart >= 0:
        annee -= 1
        ecart = ecart_temperature(datas, annee)
    return annee

print("Dernière année avec écart négatif :", derniere_annee_ecart_negatif(datas_temperature))

# =============================================================================
# QUESTION 3 : correction de moyenne_ecarts (bug : soustraction au lieu d'addition)
# =============================================================================

def moyenne_ecarts(annee_debut, annee_fin, datas):
    """
    CORRECTION : la ligne 'somme = somme - dico["écart"]' soustrayait
    les valeurs au lieu de les additionner, inversant le signe de la moyenne.
    Il faut 'somme = somme + dico["écart"]'.
    """
    somme = 0
    compteur = 0
    for dico in datas:
        if annee_debut <= dico["année"] <= annee_fin:
            somme = somme + dico["écart"]   # CORRECTION : + au lieu de -
            compteur += 1
    return somme / compteur


def prevision(datas, annee, n):
    longueur = len(datas)
    annee_debut = datas[longueur - n]["année"]
    annee_fin = datas[longueur - 1]["année"]
    moy_annees = (annee_debut + annee_fin) / 2
    moy_temperatures = moyenne_ecarts(annee_debut, annee_fin, datas)
    numerateur = 0
    denominateur = 0
    for i in range(1, n + 1):
        ecart_annee = datas[longueur - i]["année"] - moy_annees
        ecart_temp = datas[longueur - i]["écart"] - moy_temperatures
        numerateur += ecart_annee * ecart_temp
        denominateur += ecart_annee ** 2
    a = numerateur / denominateur
    b = moy_temperatures - a * moy_annees
    return a * annee + b

print(f"Prévision pour 2040 (corrigée) : {prevision(datas_temperature, 2040, 20):.2f} °C")

# =============================================================================
# QUESTION 4 : graphique – remplissage de annees et ordonnees
# =============================================================================

def graphique(datas):
    fig, ax = plt.subplots(figsize=(10, 2))
    cmap = plt.get_cmap("seismic")
    temperatures = [dico["écart"] for dico in datas]
    max_val = max(max(temperatures), -min(temperatures))
    norm = plt.Normalize(-max_val, max_val)

    # QUESTION 4 : remplissage des listes
    annees    = [dico["année"] for dico in datas]   # abscisses : une valeur par année
    ordonnees = [1 for _ in datas]                  # ordonnées : 1 pour chaque bande (hauteur uniforme)

    ax.bar(annees, ordonnees, width=1.0, color=cmap(norm(temperatures)))
    ax.set_title("Warming Stripes mondiales - Base 1901-2000")
    plt.yticks([], [])
    ax.set_xlabel("Année")
    plt.tight_layout()
    plt.show()

# graphique(datas_temperature)
