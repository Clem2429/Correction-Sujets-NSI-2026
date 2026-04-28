from donnees import reservoirs

# =============================================================================
# QUESTION 1 : est_en_penurie
# =============================================================================

def est_en_penurie(liste_reservoirs, nom):
    """Renvoie True si le réservoir nommé 'nom' a un taux de remplissage < 20 %."""
    for r in liste_reservoirs:
        if r["nom"] == nom:
            return (r["volume"] / r["capacite"]) < 0.20
    # Le nom n'a pas été trouvé (par hypothèse de l'énoncé, ne doit pas arriver)
    return False

print("Motuavai en pénurie ?", est_en_penurie(reservoirs, "Motuavai"))   # 10000/90000 ≈ 11% → True
print("Nuiavai en pénurie ?",  est_en_penurie(reservoirs, "Nuiavai"))    # 55000/100000 = 55% → False

# =============================================================================
# QUESTION 2 : volume_par_district
# =============================================================================

def volume_par_district(liste_reservoirs):
    """Renvoie un dictionnaire {district: volume_total}."""
    resultat = {}
    for r in liste_reservoirs:
        district = r["district"]
        if district not in resultat:
            resultat[district] = 0
        resultat[district] += r["volume"]
    return resultat

print("Volume par district :", volume_par_district(reservoirs))

# =============================================================================
# QUESTION 3 : tests et correction de volume_moyen
# =============================================================================

# --- Tests qui mettent en évidence le bug ---

r_test_simple = [
    {"nom": "A", "capacite": 100, "volume": 50, "district": "X"},
    {"nom": "B", "capacite": 100, "volume": 50, "district": "Y"},
]

def volume_moyen(liste_reservoirs):
    """
    CORRECTION : la version originale divisait par `len(reservoirs) - 1` au lieu
    de `len(reservoirs)`, ce qui surévaluait la moyenne d'un facteur n/(n-1).
    """
    somme_totale = 0
    for r in liste_reservoirs:
        somme_totale += r["volume"]
    return somme_totale / len(liste_reservoirs)   # CORRECTION : sans le -1

# Test 1 : au moins un réservoir (liste non vide)
assert len(r_test_simple) >= 1

# Test 2 : la moyenne ne peut pas dépasser la plus grande capacité
moy = volume_moyen(r_test_simple)
max_cap = max(r["capacite"] for r in r_test_simple)
assert moy <= max_cap, f"Moyenne {moy} > capacité max {max_cap}"

# Test 3 : résultat correct sur un cas simple (deux réservoirs à 50 L → moyenne 50)
assert volume_moyen(r_test_simple) == 50.0, f"Attendu 50.0, obtenu {volume_moyen(r_test_simple)}"

print("Tests volume_moyen : OK")
print("Volume moyen global (données réelles) :", volume_moyen(reservoirs))

# =============================================================================
# QUESTION 4 : districts vulnérables + stratégie de gestion
# =============================================================================

def districts_vulnerables(liste_reservoirs, seuil=0.80):
    """
    Identifie les districts dont le volume moyen par réservoir est inférieur à
    seuil * volume_moyen_global.
    Renvoie une liste de tuples (nom_district, volume_moyen_district).
    """
    moy_globale = volume_moyen(liste_reservoirs)
    rpd = {}
    for r in liste_reservoirs:
        d = r["district"]
        rpd.setdefault(d, []).append(r)

    vulnerables = []
    for district, res_liste in rpd.items():
        moy_district = sum(r["volume"] for r in res_liste) / len(res_liste)
        if moy_district < seuil * moy_globale:
            vulnerables.append((district, round(moy_district, 1)))
    return vulnerables

print("Districts vulnérables :", districts_vulnerables(reservoirs))

"""
Stratégie de gestion proposée (sans implémentation) :
1. Identifier les réservoirs excédentaires (taux > 80 %) dans les districts non vulnérables.
2. Calculer le volume transférable depuis ces réservoirs (sans passer sous 50 % de remplissage).
3. Prioriser les districts dont le taux est le plus bas (risque de pénurie imminent).
4. Planifier des transferts par camion citerne ou ouverture des canalisations inter-districts.
5. Réévaluer après chaque transfert pour éviter de créer de nouveaux déséquilibres.
"""
