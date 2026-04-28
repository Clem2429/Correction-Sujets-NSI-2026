donnees_test = [
    {'date': '2010-01-15', 'zone': 'Societe', 'temperature': 27.0},
    {'date': '2010-06-20', 'zone': 'Societe', 'temperature': 26.5},
    {'date': '2011-03-10', 'zone': 'Societe', 'temperature': 27.5},
    {'date': '2020-02-14', 'zone': 'Societe', 'temperature': 28.0},
    {'date': '2020-08-22', 'zone': 'Societe', 'temperature': 28.5},
    {'date': '2021-05-30', 'zone': 'Societe', 'temperature': 29.0},
    {'date': '2015-04-10', 'zone': 'Tuamotu', 'temperature': 26.8},
    {'date': '2020-07-15', 'zone': 'Tuamotu', 'temperature': 27.5},
    {'date': '2021-09-20', 'zone': 'Tuamotu', 'temperature': 28.0},
    {'date': '2020-03-15', 'zone': 'Marquises', 'temperature': 25.5},
    {'date': '2021-07-10', 'zone': 'Marquises', 'temperature': 26.0},
    {'date': '2022-11-25', 'zone': 'Marquises', 'temperature': 26.5},
]

# =============================================================================
# QUESTION 1 : temperature_moyenne
# =============================================================================

def temperature_moyenne(zone, donnees):
    """Renvoie la température moyenne de la zone, ou None si aucun relevé."""
    releves = [r['temperature'] for r in donnees if r['zone'] == zone]
    if not releves:
        return None
    return sum(releves) / len(releves)

# Vérifications rapides
assert temperature_moyenne('Societe', donnees_test) == (27.0+26.5+27.5+28.0+28.5+29.0)/6
assert temperature_moyenne('Inconnu', donnees_test) is None
print("temperature_moyenne : OK")

# =============================================================================
# QUESTION 2 : detecter_anomalies
# =============================================================================

def detecter_anomalies(zone, seuil, donnees):
    """Renvoie les dates où la température s'écarte de plus de seuil degrés de la moyenne."""
    moy = temperature_moyenne(zone, donnees)
    if moy is None:
        return []
    return [r['date'] for r in donnees if r['zone'] == zone and abs(r['temperature'] - moy) > seuil]

print("detecter_anomalies (Societe, seuil=1.0) :", detecter_anomalies('Societe', 1.0, donnees_test))

# =============================================================================
# QUESTION 3 & 4 : tests + correction de evolution_par_decennie
# =============================================================================

def evolution_par_decennie(zone, donnees):
    """
    CORRECTION : la décennie était calculée avec `annee // 10` (ex: 2010→201, 2020→202)
    au lieu de `(annee // 10) * 10` (ex: 2010→2010, 2020→2020).
    Les clés du dictionnaire étaient donc 201, 202 au lieu de 2010, 2020.
    """
    releves_zone = [r for r in donnees if r['zone'] == zone]
    if not releves_zone:
        return {}

    temperatures_par_decennie = {}
    for releve in releves_zone:
        annee = int(releve['date'].split('-')[0])
        decennie = (annee // 10) * 10   # CORRECTION : * 10 ajouté

        if decennie not in temperatures_par_decennie:
            temperatures_par_decennie[decennie] = []
        temperatures_par_decennie[decennie].append(releve['temperature'])

    moyennes = {}
    for decennie, temperatures in temperatures_par_decennie.items():
        moyennes[decennie] = round(sum(temperatures) / len(temperatures), 2)
    return moyennes


def test_zone_inexistante():
    """Test 1 : zone inexistante → dictionnaire vide."""
    resultat = evolution_par_decennie('Australes', donnees_test)
    assert resultat == {}, f"Attendu {{}}, obtenu {resultat}"
    print("test_zone_inexistante : OK")


def test_une_seule_decennie():
    """Test 2 : Marquises n'a des données qu'à partir de 2020 → une seule clé 2020."""
    resultat = evolution_par_decennie('Marquises', donnees_test)
    assert len(resultat) == 1, f"Attendu 1 décennie, obtenu {len(resultat)}"
    assert 2020 in resultat, f"Clé 2020 absente : {resultat}"
    # (25.5 + 26.0 + 26.5) / 3 = 26.0
    assert resultat[2020] == 26.0, f"Attendu 26.0, obtenu {resultat[2020]}"
    print("test_une_seule_decennie : OK")


def test_plusieurs_decennies():
    """Test 3 : Société a des données sur 2010 et 2020 → deux clés."""
    resultat = evolution_par_decennie('Societe', donnees_test)
    assert 2010 in resultat and 2020 in resultat, f"Clés attendues 2010 et 2020, obtenu {list(resultat.keys())}"
    # Décennie 2010 : 27.0, 26.5, 27.5 → 27.0
    assert resultat[2010] == 27.0, f"Attendu 27.0, obtenu {resultat[2010]}"
    # Décennie 2020 : 28.0, 28.5, 29.0 → 28.5
    assert resultat[2020] == 28.5, f"Attendu 28.5, obtenu {resultat[2020]}"
    print("test_plusieurs_decennies : OK")


test_zone_inexistante()
test_une_seule_decennie()
test_plusieurs_decennies()

print("\nÉvolution par décennie (Societe) :", evolution_par_decennie('Societe', donnees_test))
