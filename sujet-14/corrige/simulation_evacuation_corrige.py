from random import randint, shuffle
from copy import deepcopy


class Piece:

    def __init__(self, profondeur: int, largeur: int):
        self.grille = [[0 for _ in range(largeur)] for _ in range(profondeur)]
        self.i_max = profondeur - 1
        self.j_max = largeur - 1
        self.capacite = profondeur * largeur * 5
        self.sorties = []

    def ajouter_occupants(self, i: int, j: int, nb: int):
        nb_add = min(nb, 5 - self.grille[i][j])
        if nb_add > 0:
            self.grille[i][j] = self.grille[i][j] + nb_add
        return nb_add

    # QUESTION 1 : nb_occupants_restants
    def nb_occupants_restants(self) -> int:
        """Renvoie le nombre total d'occupants restants dans la pièce."""
        total = 0
        for ligne in self.grille:
            for case in ligne:
                total += case
        return total
        # Version concise avec sum : return sum(case for ligne in self.grille for case in ligne)

    # QUESTION 3 : ajouter_sortie (directions S et E ajoutées)
    def ajouter_sortie(self, direction: str, position: int):
        """Permet d'ajouter des sorties dans les 4 directions (N, S, E, O)."""
        if direction == "N":
            self.sorties.append((0, position))
        elif direction == "O":
            self.sorties.append((position, 0))
        elif direction == "S":
            # CORRECTION : la sortie Sud est sur la dernière ligne, à la colonne 'position'
            self.sorties.append((self.i_max, position))
        elif direction == "E":
            # CORRECTION : la sortie Est est sur la ligne 'position', à la dernière colonne
            self.sorties.append((position, self.j_max))

    # QUESTION 4 : choix_sortie corrigée
    def choix_sortie(self, i: int, j: int) -> tuple:
        """Renvoie la sortie la plus proche (distance de Manhattan) pour la case (i, j)."""
        def distance_de_manhattan(destination):
            return abs(i - destination[0]) + abs(j - destination[1])

        assert len(self.sorties) > 0, "Aucune sortie"
        choix = self.sorties[0]
        distance_min = distance_de_manhattan(choix)  # CORRECTION : variable renommée distance_min
        for k in range(1, len(self.sorties)):
            autre_sortie = self.sorties[k]
            d2 = distance_de_manhattan(autre_sortie)  # CORRECTION : d2 était non défini
            if d2 < distance_min:                     # CORRECTION : condition était k < 0 (jamais vraie)
                choix = autre_sortie
                distance_min = d2
        return choix

    def deplacer(self, i, j, nb, direction, silencieux=True):
        d = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
        nv_i, nv_j = i + d[direction][0], j + d[direction][1]
        nb_dep = min(nb, 5 - self.grille[nv_i][nv_j], self.grille[i][j])
        if nb_dep > 0:
            if not silencieux:
                print("déplacement de ", nb_dep, " occupant(s) (", i, ",", j, ") vers ", direction)
            self.grille[i][j] = self.grille[i][j] - nb_dep
            self.grille[nv_i][nv_j] = self.grille[nv_i][nv_j] + nb_dep
        return nb_dep

    def alerter(self, silencieux=True):
        old_grille = deepcopy(self.grille)
        modif = False
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                if old_grille[i][j] > 0:
                    sortie_i, sortie_j = self.choix_sortie(i, j)
                    dx, dy = sortie_j - j, sortie_i - i
                    if dx == 0 and dy == 0:
                        if not silencieux:
                            print("évacuation d'un occupant (", i, ",", j, ")")
                        self.grille[i][j] = self.grille[i][j] - 1
                        nb_dep = 1
                    else:
                        mvt_possibles = []
                        if dx > 0:
                            mvt_possibles.append("E")
                        elif dx < 0 and j > 0:
                            mvt_possibles.append("O")
                        if dy > 0:
                            mvt_possibles.append("S")
                        elif dy < 0 and i > 0:
                            mvt_possibles.append("N")
                        shuffle(mvt_possibles)
                        nb_dep = self.deplacer(i, j, old_grille[i][j], mvt_possibles[0], silencieux)
                        if nb_dep == 0 and len(mvt_possibles) > 1:
                            nb_dep = self.deplacer(i, j, old_grille[i][j], mvt_possibles[1], silencieux)
                    if nb_dep > 0:
                        modif = True
        return modif

    def __str__(self):
        s = "  "
        for j in range(self.j_max + 1):
            if (0, j) in self.sorties:
                s = s + "P  "
            else:
                s = s + "   "
        s = s + "\n"
        for i in range(len(self.grille)):
            if (i, 0) in self.sorties:
                s = s + "P"
            else:
                s = s + " "
            s = s + str(self.grille[i])
            if i != 0 and i != self.i_max and (i, self.j_max) in self.sorties:
                s = s + "P\n"
            else:
                s = s + "\n"
        s = s + "  "
        for j in range(self.j_max + 1):
            if (self.i_max, j) in self.sorties:
                s = s + "P  "
            else:
                s = s + "   "
        return s + "\n"


# QUESTION 2 : fonction evacuation
def evacuation(p: Piece, silencieux: bool = True) -> int:
    """Simule l'évacuation complète de la pièce et renvoie le nombre de tours nécessaires."""
    nb_tours = 0
    while p.nb_occupants_restants() > 0:
        a_bouge = p.alerter(silencieux)
        nb_tours += 1
        if not silencieux:
            print(p)
        if not a_bouge:
            # Plus aucun mouvement possible (blocage) — sécurité anti-boucle infinie
            break
    return nb_tours


# ---- Tests ----
def test_nb_occupants_restants():
    p1 = Piece(5, 7)
    p1.ajouter_sortie("N", 5)
    reussite = True
    if p1.nb_occupants_restants() != 0:
        print("La méthode nb_restants devrait renvoyer 0 quand la pièce est vide.")
        reussite = False
    n1 = randint(1, 5)
    cases_occupees = {(0, 3): 4, (0, 1): 2, (3, 4): 3, (4, 0): n1, (4, 3): 2}
    for c in cases_occupees:
        p1.ajouter_occupants(c[0], c[1], cases_occupees[c])
    if p1.nb_occupants_restants() != 11 + n1:
        print("La méthode nb_restants renvoie", p1.nb_occupants_restants(), " au lieu", 11 + n1)
        reussite = False
    if reussite:
        print("nb_occupants_restants : OK")


def test_evacuation(silencieux=True):
    p1 = Piece(5, 7)
    p1.ajouter_sortie("N", 5)
    situations = [
        {"nom": "essai1", "cases_occupees": {(0, 3): 3, (1, 1): 1, (3, 2): 5}, "temps_attendu": 11},
        {"nom": "essai2", "cases_occupees": {(0, 3): 4, (0, 1): 2, (3, 4): 3, (4, 0): 1, (4, 3): 2}, "temps_attendu": 14},
        {"nom": "essai3", "cases_occupees": {(0, 3): 1, (0, 1): 2, (3, 4): 1, (4, 0): 3, (4, 3): 5}, "temps_attendu": 15},
    ]
    verif = True
    for s in situations:
        for c, nb in s["cases_occupees"].items():
            p1.ajouter_occupants(c[0], c[1], nb)
        nbT = evacuation(p1, silencieux)
        if nbT != s["temps_attendu"]:
            print(f"evacuation renvoie {nbT} au lieu de {s['temps_attendu']} pour {s['nom']}")
            verif = False
    if verif:
        print("evacuation : OK")


def test_ajouter_sortie():
    p1 = Piece(5, 7)
    p1.ajouter_sortie("N", 5)
    n1 = randint(1, 5)
    p1.ajouter_sortie("S", n1)
    n2 = randint(1, 5)
    p1.ajouter_sortie("E", n2)
    p1.ajouter_sortie("O", 1)
    if p1.sorties == [(0, 5), (4, n1), (n2, 6), (1, 0)]:
        print("ajouter_sortie : OK")
    else:
        print("ajouter_sortie : ERREUR", p1.sorties)


def test_choix_sortie():
    p1 = Piece(5, 7)
    p1.sorties = [(0, 5), (4, 1), (3, 6), (1, 0)]
    try:
        assert p1.choix_sortie(0, 3) == (0, 5)
        assert p1.choix_sortie(0, 1) == (1, 0)
        assert p1.choix_sortie(1, 2) == (1, 0)
        assert p1.choix_sortie(3, 4) == (3, 6)
        assert p1.choix_sortie(4, 0) == (4, 1)
        assert p1.choix_sortie(4, 3) == (4, 1)
        print("choix_sortie : OK")
    except AssertionError:
        print("choix_sortie : ERREUR sur au moins un test")


if __name__ == "__main__":
    test_nb_occupants_restants()
    test_evacuation(True)
    test_ajouter_sortie()
    test_choix_sortie()
