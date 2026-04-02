import os
import os.path
import json

########### Fonctions données ###########

def chargement_json(nom_fichier):
    """Charge le contenu d'un fichier JSON dans un dictionnaire Python renvoyé"""
    with open(nom_fichier, "r", encoding="utf8") as curseur:
        return json.load(curseur)


def sauvegarde_json(dictionnaire, nom_fichier):
    """Sauvegarde le contenu d'un dictionnaire dans un fichier JSON"""
    with open(nom_fichier, "w", encoding="utf8") as curseur:
        json.dump(dictionnaire, curseur)


def est_dictionnaire(objet):
    """Teste si un objet est de type dictionnaire"""
    return isinstance(objet, dict)


##########################################


### Première fonction à implémenter après avoir découvert le fichier JSON agrégé
### Cf fichier `empreinte_ada_agr.json`
def total_simple(empreinte):
    """Fonction qui renvoie l'empreinte carbone totale d'un dictionnaire associant
    une empreinte carbone à des noms de catégories"""
    s = 0
    for key in empreinte:
        s += empreinte[key]
    return s

def test_total_simple():
    e_ada = chargement_json("empreinte_ada_agr.json")
    if est_dictionnaire(e_ada):
        # On a calculé depuis le fichier, on doit obtenir 7252 donc on prévient
        # l'erreur avant le return.
        assert total_simple(e_ada) == 7252, "Echec du calcul"
        return total_simple(e_ada)



### Deuxième fonction : il faut la récursivité pour le cas des sous-catégories
### Cf fichier `empreinte_ada.json`
def total_rec(empreinte):
    '''Fonction récursive qui renvoie l'empreinte carbone totale représentée
    par un dictionnaire dont les valeurs peuvent aussi être des dictionnaires'''
    s = 0
    for key in empreinte:
        if not est_dictionnaire(empreinte[key]):
            s += empreinte[key]
        else:
            s += total_rec(empreinte[key])
    return s
        
def test_total_rec():
    test_dico1 = {"a": 1, "d": 2}
    assert total_rec(test_dico1) == 3
    test_dico2 = {"a": {"b": 1, "c": 2}, "d": {"e": 3}}
    assert total_rec(test_dico2) == 6
    # Test ajouté avec l'empreinte totale de Ada (= 7252) :
    e_ada = chargement_json("empreinte_ada.json")
    assert total_rec(e_ada) == 7252, "Echec du Test pour données complètes"

# ==========================================
# Fonction à analyser et corriger (Question 3)
# ==========================================

def alerte_valeur_aberrante(empreinte, limite):
    """
    Fonction censée déterminer si au moins une valeur du dictionnaire
    dépasse strictement la limite donnée.
    """
    if empreinte == {}:
        print("Votre dictionnaire est vide.")
        return False
    for valeur in empreinte.values():
        if est_dictionnaire(valeur):
            if alerte_valeur_aberrante(valeur, limite):
                return True
        else:
            if valeur > limite:
                return True
    return False

def tests_valeur_aberrante():
    dico_simple = {
        "valeur_a": 2,
        "valeur_b": 5,
        "valeur_c": 10,
        "valeur_d": 0,
        "valeur_e": 46
     }
    # T1 - On teste avec un dictionnaire simple avec une valeur aberrante :
    assert alerte_valeur_aberrante(dico_simple, 45) == True,"Echec Test 1"

    #T2 - On teste avec un dictionnaire simple sans une valeur aberrante :
    assert alerte_valeur_aberrante(dico_simple, 50) == False,"Echec Test 2"

    #T3 - On teste avec un dictionnaire simple dont la valeur max est la limite :
    assert alerte_valeur_aberrante(dico_simple, 46) == False,"Echec Test 3"

    dico_complexe = {
        "valeur_a": 2,
        "valeur_b": {
            "valeur_ba": 3,
            "valeur_bb": 19028,
            "valeur_bc": 0,
            "valeur_bd": 1039
        },
        "valeur_c": 10,
        "valeur_d": {
            "valeur_da": 2,
            "valeur_db": 1892
        },
        "valeur_e": {
            "valeur_ea": {
                "valeur_eaa": 2,
                "valeur_eab": {
                    "valeur_eaba": 20001
                },
                "valeur_eac": 2900
            },
            "valeur_eb": 29
        }
     }
    # T4 - On teste avec un dictionnaire complexe avec une valeur aberrante :
    assert alerte_valeur_aberrante(dico_complexe, 20000) == True, "Echec Test 4"

    # T5 - On teste avec un dictionnaire complexe sans une valeur aberrante :
    assert alerte_valeur_aberrante(dico_complexe, 900000) == False, "Echec Test 5"

    dico_nul = {}
    # T6 - On teste avec un dictionnaire nul :
    assert alerte_valeur_aberrante(dico_nul, 0) == False, "Echec Test 6"

    dico_negatif = {
        "valeur_a": -2,
        "valeur_b": {
            "valeur_ba": 3,
            "valeur_bb": -19028,
            "valeur_bc": 0,
            "valeur_bd": -1039
        },
        "valeur_c": -10,
        "valeur_d": {
            "valeur_da": 2,
            "valeur_db": -1892
        },
        "valeur_e": {
            "valeur_ea": {
                "valeur_eaa": 2,
                "valeur_eab": {
                    "valeur_eaba": 20001
                },
                "valeur_eac": -2900
            },
            "valeur_eb": -29
        }
     }

    # T7 - On teste avec un dictionnaire complexe negatif avec une valeur aberrante :
    assert alerte_valeur_aberrante(dico_negatif, -2) == True, "Echec Test 7"

    # T8 - On teste avec un dictionnaire complexe negatif sans une valeur aberrante :
    assert alerte_valeur_aberrante(dico_negatif, 900000) == False, "Echec Test 8"  
