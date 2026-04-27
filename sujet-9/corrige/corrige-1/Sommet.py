import math


class Sommet:

    """
    Représente un sommet (point) dans l'espace 3D.
    """

    def __init__(self, x, y, z):
        """
        Initialise un sommet avec ses coordonnées.
        """
        self.x = x
        self.y = y
        self.z = z

    def est_adjacent(self, sommet):
        """
        Indique si le sommet courant est adjacent à un autre sommet.
        """
        nb_changement = 0
        if self.x != sommet.x:
            nb_changement = nb_changement + 1
        if self.y != sommet.y:
            nb_changement = nb_changement + 1
        if self.z != sommet.z:
            nb_changement = nb_changement + 1
        return nb_changement == 1


#############################################################################
# Écrire le code de la méthode distance de la question 1                    #
#############################################################################
def distance(Sommet_a, Sommet_b): 
    assert isinstance(Sommet_a, Sommet) and isinstance(Sommet_b, Sommet), "les arguments doivent être des type de la classe Sommet"
    s = (Sommet_a.x - Sommet_b.x)**2 + (Sommet_a.y - Sommet_b.y)**2 + (Sommet_a.z - Sommet_b.z)**2
    return math.sqrt(s)
#############################################################################
# Programme pour tester votre méthode de la question 1                                  #
#############################################################################
s1 = Sommet(0, 0, 0)
s2 = Sommet(3, 4, 0)
# le vecteur S1S2 doit donnée sqrt(25) ==> 5
assert distance(s1, s2) == 5.0

