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
    if est_dictionnaire(empreinte):
        somme = 0
        for values in empreinte.values():
            somme += values
        
        return somme
    else: 
        raise TypeError("vous devez mettre un dictionnaire")

def total_simple_test():
    dic = chargement_json('empreinte_ada_agr.json')
    assert total_simple(dic) == 7252

total_simple_test()
### Deuxième fonction : il faut la récursivité pour le cas des sous-catégories
### Cf fichier `empreinte_ada.json`
def total_rec(empreinte):
    """Fonction récursive qui renvoie l'empreinte carbone totale représentée
    par un dictionnaire dont les valeurs peuvent aussi être des dictionnaires"""
    S = 0
    for values in empreinte.values():
        if est_dictionnaire(values):
            S = S + total_rec(values)
        else:
            S = S + values
    return S
          


def test_total_rec():
    test_dico1 = {"a": 1, "d": 2}
    assert total_rec(test_dico1) == 3
    test_dico2 = {"a": {"b": 1, "c": 2}, "d": {"e": 3}}
    assert total_rec(test_dico2) == 6
    dico_ada = chargement_json('empreinte_ada.json')
    assert total_rec(dico_ada) == 7252

test_total_rec()

# ==========================================
# Fonction à analyser et corriger (Question 3)
# ==========================================

def alerte_valeur_aberrante(empreinte, limite):
    """
    Fonction censée déterminer si au moins une valeur du dictionnaire
    dépasse strictement la limite donnée.
    """
    for categorie, valeur in empreinte.items():
        print(valeur)
        if est_dictionnaire(valeur):
            return alerte_valeur_aberrante(valeur, limite)
        else:
            if valeur > limite:
                return True
    return False


"""
le problème dans cette fonction c'est que si l'on rencontre un dictionnaire on arrête la fouille actuelle et 
on part sur le nouveau donc toutes les valeurs ne sont pas analysées
"""

def correction_alerte_valeur_aberrante(empreinte, limite):
    """
    Fonction censée déterminer si au moins une valeur du dictionnaire
    dépasse strictement la limite donnée.
    """
    p = False
    for categorie, valeur in empreinte.items():
        if est_dictionnaire(valeur):
            p = alerte_valeur_aberrante(valeur, limite)
            if p:
                return p
        else:
            if valeur > limite:
                return True
    return False

def test_correction_alerte_valeur_aberrante():  
    dic1 = {"a": {}, "b": {"c": 4000}}
    assert correction_alerte_valeur_aberrante(dic1, 1000) #sous_dictionnaire droit et faux donc doit mettre True

    dic2 = {"a": 400, "b": {"C": {}, "D": {'r': 4000}}} 
    assert not  correction_alerte_valeur_aberrante(dic2, 5000) #doit renvoyer False

    dic3 = {"a": 4000}
    assert correction_alerte_valeur_aberrante(dic3, 100) #doit renvoyer True
