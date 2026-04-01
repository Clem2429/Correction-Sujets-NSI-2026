#############################################################################
# Jeux de données fournis                                                   #
#############################################################################
from plantes import plantes
from mesures import mesures

#############################################################################
# Écrire le code de la fonction croissance_moyenne de la question 1         #
#############################################################################

def croissance_moyenne(plantes):
    if plantes == []:
        return None
    s = 0
    n = 0
    for plante in plantes:
        s += plante.croissance
        n += 1
    return s/n

def test_croissance_moyenne():
    assert croissance_moyenne(plantes) == 79.0, "Echec Test 1, données plantes"
    assert croissance_moyenne([]) == None, "Echec Test 2, liste vide"

#############################################################################
# Écrire le code de la fonction dictionnaire_mesure de la question 2      #
#############################################################################

def dictionnaire_mesure(plantes, mesures):
    dico = {}
    for plante in plantes:
        dico[plante.nom] = []
        
    for mesure in mesures:
        if mesure['plante'] in dico:
            dico[mesure['plante']].append(mesure)
        else:
            dico[mesure['plante']] = []
    return dico

def test_dictionnaire_mesure():
    from plantes import Plante
    plantes_liste = [
        Plante("Basilic", "Ocimum basilicum", 60, 40, "plein soleil"),
        Plante("Tomate", "Solanum lycopersicum", 80, 100, "plein soleil"),
        Plante("Iris", "Iris", 80, 50, "plein soleil")
    ]
    mesures = [
        {'jour': 1, 'plante': 'Basilic', 'hauteur': 0.85, 'temperature': 29.3, 'humidite': 50.89},
        {'jour': 1, 'plante': 'Tomate', 'hauteur': 1.27, 'temperature': 21.51, 'humidite': 47.19}
    ]
    assert dictionnaire_mesure(plantes_liste, mesures) == {"Basilic": [{"plante": "Basilic","jour": 1,"hauteur": 0.85,"temperature": 29.3,"humidite": 50.89,}],"Tomate": [{"plante": "Tomate","jour": 1,"hauteur": 1.27,"temperature": 21.51,"humidite": 47.19,}],"Iris": []}

#############################################################################
# Fonction défaillante à analyser et corriger pour les questions 3 et 4     #
#############################################################################

def purger_mesures_extremes(liste_mesures):
    """
    Supprime de la liste toutes les mesures dont la température 
    n'est pas comprise entre 20 et 25°C inclus.
    """
    copie = liste_mesures.copy()
    for mesure in copie:
        if mesure['temperature'] < 20 or mesure['temperature'] > 25:
            liste_mesures.remove(mesure)
    return liste_mesures

def test_purger():
    mesures_test = [
         {'jour': 1, 'plante': 'Basilic', 'temperature': 18.0},
         {'jour': 2, 'plante': 'Basilic', 'temperature': 19.0},
         {'jour': 3, 'plante': 'Basilic', 'temperature': 22.0},
         {'jour': 4, 'plante': 'Basilic', 'temperature': 28.0},
         {'jour': 5, 'plante': 'Basilic', 'temperature': 29.0}
    ]

    purger_mesures_extremes(mesures_test)

    print("Résultat après la purge :")
    for m in mesures_test:
        print(f"Jour {m['jour']} : {m['temperature']}°C")
