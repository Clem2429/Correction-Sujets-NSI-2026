import sqlite3

DB_PATH = "cabinet.sqlite"

# =============================================================================
# QUESTION 1 : normalisation_tel
# =============================================================================

def normalisation_tel(tel):
    """Renvoie le numéro de téléphone en ne conservant que les chiffres."""
    return ''.join(c for c in tel if c.isdigit())

def test_normalisation_tel():
    assert normalisation_tel("06 12 99 90 12") == "0612999012"
    assert normalisation_tel("02 12 99 90 12") == "0212999012"
    assert normalisation_tel("02.12.99.90.12") == "0212999012"
    assert normalisation_tel("0.6.12.99.90.12") == "0612999012"
    assert normalisation_tel("06-12-99-90-12") == "0612999012"
    assert normalisation_tel("(0)6.12.99-90-12 gilbert") == "0612999012"
    assert normalisation_tel("061299901") == "061299901"
    assert normalisation_tel("06129990123") == "06129990123"
    print("Les tests de normalisation_tel sont passés.")

test_normalisation_tel()

# =============================================================================
# QUESTION 2 : jeu de tests pour validation_tel
# =============================================================================

def validation_tel(tel):
    """Valide un numéro de portable français (06 ou 07, 10 chiffres)."""
    if len(tel) != 10:
        return False
    if tel[0] != "0":
        return False
    if tel[1] not in ("6", "7"):
        return False
    return True

# Jeu de tests
assert validation_tel("0612999012") == True    # 06 valide
assert validation_tel("0712999012") == True    # 07 valide
assert validation_tel("0212999012") == False   # fixe → invalide
assert validation_tel("061299901")  == False   # 9 chiffres → invalide
assert validation_tel("06129990123") == False  # 11 chiffres → invalide
assert validation_tel("1612999012") == False   # ne commence pas par 0
print("Les tests de validation_tel sont passés.")

# =============================================================================
# QUESTION 3 : consultation_vaccination_chat
# =============================================================================

def proprietaires_animaux_nes_apres(date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    resultat = cursor.execute(
        """
    SELECT proprietaire.nom, proprietaire.prenom
    FROM proprietaire
        JOIN animal ON proprietaire.id = animal.id_proprietaire
    WHERE animal.date_naissance > ?
    ORDER BY proprietaire.nom, proprietaire.prenom;
    """,
        (date,),
    )
    return list(resultat)


def consultation_vaccination_chat(date):
    """
    Renvoie les consultations de vaccination de chats après la date donnée.
    Champs retournés : (id_animal, nom_animal, tel_proprietaire, date_consultation)
    triés par id_animal puis date_consultation croissants.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    resultat = cursor.execute(
        """
        SELECT animal.id, animal.nom, proprietaire.telephone, consultation.date
        FROM consultation
            JOIN animal ON consultation.id_animal = animal.id
            JOIN proprietaire ON animal.id_proprietaire = proprietaire.id
        WHERE animal.espece = 'chat'
          AND consultation.motif = 'vaccination'
          AND consultation.date > ?
        ORDER BY animal.id, consultation.date;
        """,
        (date,),
    )
    return list(resultat)


def test_consultation_vaccination_chat():
    vaccinations = consultation_vaccination_chat("20240923")
    assert len(vaccinations) == 118
    assert vaccinations[0] == (16, "Plume", "0.6.36.96.89.83", "20241024")
    assert vaccinations[1] == (16, "Plume", "0.6.36.96.89.83", "20251125")
    assert vaccinations[2] == (17, "Gollum", "0.6.36.96.89.83", "20250113")
    print("Les tests de consultation_vaccination_chat sont passés.")

test_consultation_vaccination_chat()

# =============================================================================
# QUESTION 4 : correction de derniere_vaccination
# =============================================================================

def derniere_vaccination(consultations):
    """
    CORRECTION : la condition était `date < derniere[id_animal][3]`
    ce qui conservait la date la PLUS ANCIENNE au lieu de la plus récente.
    Il faut inverser : mettre à jour si date > derniere[id_animal][3].
    """
    derniere = {}
    for consult in consultations:
        id_animal = consult[0]
        date = consult[3]
        if id_animal not in derniere:
            derniere[id_animal] = consult
        elif date > derniere[id_animal][3]:   # CORRECTION : > au lieu de <
            derniere[id_animal] = consult
    return derniere


def test_derniere_vaccination():
    consultations_pour_test = [
        (16, "Plume", "0.6.36.96.89.83", "20241024"),
        (16, "Plume", "0.6.36.96.89.83", "20251125"),
        (17, "Gollum", "0.6.36.96.89.83", "20250113"),
        (26, "Olympe", "(0)4 73 98 01 23", "20250109"),
        (32, "Chopin", "06.37.97.66.64", "20241201"),
        (32, "Chopin", "06.37.97.66.64", "20251119"),
        (34, "Jazz", "0.6.37.51.65.52", "20250801"),
        (35, "Tango", "0324182", "20250706"),
        (38, "Loulou", "05-35-95-87-54", "20250209"),
        (39, "Tango", "07.45.48.02.42", "20250329"),
        (40, "Sésame", "07.45.48.02.42", "20250228"),
        (41, "Pixel", "0130709285", "20241204"),
        (41, "Pixel", "0130709285", "20251222"),
    ]
    assert derniere_vaccination(consultations_pour_test) == {
        16: (16, "Plume", "0.6.36.96.89.83", "20251125"),
        17: (17, "Gollum", "0.6.36.96.89.83", "20250113"),
        26: (26, "Olympe", "(0)4 73 98 01 23", "20250109"),
        32: (32, "Chopin", "06.37.97.66.64", "20251119"),
        34: (34, "Jazz", "0.6.37.51.65.52", "20250801"),
        35: (35, "Tango", "0324182", "20250706"),
        38: (38, "Loulou", "05-35-95-87-54", "20250209"),
        39: (39, "Tango", "07.45.48.02.42", "20250329"),
        40: (40, "Sésame", "07.45.48.02.42", "20250228"),
        41: (41, "Pixel", "0130709285", "20251222"),
    }
    print("Les tests de derniere_vaccination sont passés.")

test_derniere_vaccination()
