def recupere_donnees_fichier_csv(nom_fichier):
    """ Fonction qui récupère les données relevées du ballon sonde sans les en-têtes de la 1ère ligne """
    altitudes = []
    temperatures = []
    longitudes = []
    latitudes = []
    contenu_fichier = open(nom_fichier, 'r')
    contenu_fichier.readline()
    for ligne in contenu_fichier.readlines():
        ligne = ligne.rstrip()
        listeValeurs = ligne.split(";")
        altitudes.append(int(listeValeurs[0]))
        temperatures.append(float(listeValeurs[1]))
        longitudes.append(float(listeValeurs[2]))
        latitudes.append(float(listeValeurs[3]))
    return altitudes, temperatures, longitudes, latitudes


def genere_kml(liste_longitudes, liste_latitudes):
    """ Génère un fichier KML - VERSION CORRIGEE (Question 6 : balise </kml> ajoutée) """
    # Question 4 : assertion sur les longueurs
    assert len(liste_longitudes) == len(liste_latitudes), \
        "Les deux listes doivent avoir la même longueur"

    fichier_kml = open('ballon sonde.kml', 'w')
    entete_fichier = '<?xml version="1.0" encoding="UTF-8"?>\n'
    entete_fichier += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    entete_fichier += '<Document>\n'
    entete_fichier += '<n>Trajectoire ballon sonde</n>\n'
    fichier_kml.write(entete_fichier)
    for i in range(len(liste_longitudes)):
        corps_fichier = '<Placemark>\n'
        corps_fichier += f'<n>Point {i}</n>\n'
        corps_fichier += '<Point>\n'
        corps_fichier += f'<coordinates>{liste_longitudes[i]},{liste_latitudes[i]}</coordinates>\n'
        corps_fichier += '</Point>\n'
        corps_fichier += '</Placemark>\n'
        fichier_kml.write(corps_fichier)
    bas_fichier = '</Document>\n'
    bas_fichier += '</kml>\n'    # CORRECTION Question 6 : balise de fermeture manquante
    fichier_kml.write(bas_fichier)
    fichier_kml.close()


# QUESTION 1 : récupération des données
altitudes, temperatures, longitudes, latitudes = recupere_donnees_fichier_csv("releves_ballon_sonde.csv")


# QUESTION 2 : conversion Kelvin → Celsius
def conversion_K_en_C(liste_temperatures):
    """Convertit une liste de températures en Kelvin en degrés Celsius, arrondies à 1 décimale."""
    return [round(t - 273.15, 1) for t in liste_temperatures]

# Test Question 2
temperatures_C = conversion_K_en_C(temperatures)
print("Test conversion (288.15 K) :", conversion_K_en_C([288.15]))  # Attendu : [15.0]
print("Températures converties :", temperatures_C)


# QUESTION 3 : altitude la plus froide
def altitude_la_plus_froide(liste_altitudes, liste_temperatures):
    """
    Renvoie un tuple (temperature_min, [altitudes correspondantes]).
    Si plusieurs altitudes partagent la même température minimale, toutes sont retournées.
    """
    temp_min = min(liste_temperatures)
    altitudes_froides = [
        liste_altitudes[i]
        for i in range(len(liste_temperatures))
        if liste_temperatures[i] == temp_min
    ]
    return (temp_min, altitudes_froides)

# Tests Question 3
print(altitude_la_plus_froide([7000, 10125, 13896, 14211], [-35.2, -52.1, -57.4, -57.4]))
# Attendu : (-57.4, [13896, 14211])
print(altitude_la_plus_froide([6000, 7250, 11542, 15214, 17300], [-33.7, -45, -53, -58.5, -60.1]))
# Attendu : (-60.1, [17300])

# Sur les données réelles
print("\nAltitude la plus froide (données réelles) :", altitude_la_plus_froide(altitudes, temperatures_C))


# QUESTION 5 : appel de genere_kml
genere_kml(longitudes, latitudes)
print("Fichier KML généré.")
