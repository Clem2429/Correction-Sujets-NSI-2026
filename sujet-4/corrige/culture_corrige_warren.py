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
    total = 0
    plante_t = len(plantes)
    for plante in plantes: 
        total += plante.croissance
    return total / plante_t

assert croissance_moyenne(plantes) == 79.0
assert croissance_moyenne([]) == None


#############################################################################
# Écrire le code de la fonction dictionnaire_mesure de la question 2      #
#############################################################################

def dictionnaire_mesure(plantes, mesures): 
    dict1 = {}
    for plante in plantes:
        for mesure in mesures:
            if mesure['plante'] == plante.nom:
                if plante.nom in dict1:
                    dict1[plante.nom].append(mesure)
                else:
                    dict1[plante.nom] = [mesure]
            else:
                if not plante.nom in dict1:
                    dict1[plante.nom] = []
    return dict1




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
        if not (20 < mesure['temperature'] < 25): 
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

test_purger()



