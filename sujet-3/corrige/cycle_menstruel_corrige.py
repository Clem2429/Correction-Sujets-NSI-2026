import calendar

#############################################################################
# Écrire le code de la fonction est_bissextile de la question 1             #
#############################################################################

def est_bissextile(annee):
    '''Renvoie un booléen indiquant si l'année en argument est bissextile.'''
    if annee%400 == 0:
        return True
    elif annee%4 == 0 and annee%100 != 0:
        return True
    else:
        return False

#############################################################################
# Écrire le code de la fonction determiner_phase de la question 2           #
#############################################################################

def determiner_phase(i):
    '''Renvoie le numéro de la phase associée au jour i d'un cycle.'''
    assert 1 <= i <= 28, "Le jour doit être compris entre 1 et 28 inclus."
    if 1 <= i <= 5:
        return 1
    elif 6 <= i <= 13:
        return 2
    elif i == 14:
        return 3
    else:
        return 4

#############################################################################
# Fonctions fournies pour la question 3                                     #
#############################################################################
def jours_dans_mois(annee, mois):
    """Renvoie le nombre de jours dans un mois donné d'une année donnée.
       Utilise le module calendar pour gérer les années bissextiles."""
    if mois == 2:  # février
        return 29 if calendar.isleap(annee) else 28
    elif mois in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    else:
        return 30

def ajouter_jours(date, nb_jours):
    """Ajoute nb_jours à une date donnée et renvoie la nouvelle date.
       La date est représentée par un tuple (jour, mois, année)."""
    jour, mois, annee = date
    jour = jour + nb_jours

    # Ajustement du jour et du mois si dépassement
    while jour > jours_dans_mois(annee, mois):
        jour = jour - jours_dans_mois(annee, mois)
        mois = mois + 1
        if mois > 12:  # passage à l'année suivante
            mois = 1
            annee = annee + 1

    return (jour, mois, annee)

# Voici un ensemble fourni de tests pour la fonction ajouter_jours :
def test_ajouter_jours():
    # 1 - (Déjà présent) Ajout de jours dans le même mois :              
    assert ajouter_jours((7, 9, 2025), 3) == (10, 9, 2025), "Echec Test 1"

    #2 - Ajout de jours qui font changer de mois (30 jours):
    assert ajouter_jours((25, 4, 2025), 10) == (5, 5, 2025), "Echec Test 2"

    #3 - Ajout de jours qui font changer de mois (31 jours):
    assert ajouter_jours((25, 7, 2025), 10) == (4, 8, 2025), "Echec Test 3"

    #4 - Ajout de jours qui font changer d'année (365 jours):
    assert ajouter_jours((25, 12, 2025), 10) == (4, 1, 2026), "Echec Test 4"

    #5 - Ajout de jours qui font changer d'année (366 jours) :
    assert ajouter_jours((25, 12, 2024), 10) == (4, 1, 2025), "Echec Test 5"

    #6 - Ajout de jours qui font changer de mois et d'année (40 jours) :
    assert ajouter_jours((25, 12, 2024), 40) == (3, 2, 2025), "Echec Test 6"

    #7 - Ajout de jours qui font changer de mois et d'année (vers février en année bissextile) :
    assert ajouter_jours((25, 12, 2024), 66) == (1, 3, 2025), "Echec Test 7"

    #8 - Ajout d'une année complète (année bissextile) :
    assert ajouter_jours((1, 1, 2024), 366) == (1, 1, 2025), "Echec Test 8"

    #9 - Ajout d'une année complète (année non bissextile) :
    assert ajouter_jours((1, 1, 2025), 365) == (1, 1, 2026), "Echec Test 9"

    #10 - Ajout de jours en février dans une année bissextile :
    assert ajouter_jours((25, 2, 2024), 5) == (1, 3, 2024), "Echec Test 10"

    #11 - Ajout de jours en février dans une année non bissextile :
    assert ajouter_jours((25, 2, 2025), 5) ==  (2, 3, 2025), "Echec Test 11"

    #12 - Ajout de 0 jour :
    assert ajouter_jours((25, 2, 2024), 0) == (25, 2, 2024), "Echec Test 12"
    
#############################################################################
# Fonction fournie pour la question 4                                       #
#############################################################################
# Fonction corrigée :
def calendrier_cycles(date_regles):
    """Renvoie une chaîne de caractère contenant au format iCalendar, l'ensemble
    des dates de début de règles qui se présentent dans les 100 jours suivants 
    `date_regles`, date incluse.

    Hypothèse : cycle régulier de 28 jours. """

    cal_lignes = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:']

    date_courante = date_regles
    jours_ecoules = 0

    # On ajoute les dates tant que l'on ne dépasse pas 100 jours écoulés
    while jours_ecoules <= 100:
        jour, mois, annee = date_courante  
        cal_lignes.append('BEGIN:VEVENT')
        cal_lignes.append('SUMMARY: Règles')
        # CORRECTION :
        date = ""
        str_mois = ""
        str_jour = ""
        if 0 < len(str(annee)) < 4:
            return "Année invalide, elle doit contenir 4 chiffres."
        if len(str(mois)) < 2:
            str_mois = "0"+str(mois)
        else:
            str_mois = str(mois)
        if len(str(jour)) < 2:
            str_jour = "0"+str(jour)
        else:
            str_jour = str(jour)
        date = str(annee) + str_mois + str_jour
        # FIN DE CORRECTION
        cal_lignes.append('DTSTART:'+date)
        cal_lignes.append('END:VEVENT')
        date_courante = ajouter_jours(date_courante, 28)
        jours_ecoules += 28 

    cal_lignes.append('END:VCALENDAR')

    # La méthode join va renvoyer ici une unique chaîne contenant toutes les
    # chaînes de la liste séparées par des sauts de lignes.
    return '\n'.join(cal_lignes)

def test_calendrier_cycles():
    '''Crée un calendrier et le charge avec le module ics pour vérifier sa
    validité.

    Nécessite que le module ics soit présent sur la machine (pip install ics).
    '''
    from ics import Calendar
    c = calendrier_cycles( (12,3,2026) )
    print(c)
    cal = Calendar(c)
    print(cal.events)
