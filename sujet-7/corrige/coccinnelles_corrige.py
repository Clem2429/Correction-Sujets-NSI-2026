import random


class Coccinelle:
    def __init__(self, sexe, age, niv_nutrition):
        self.age = age
        self.esperance_de_vie = random.randint(200, 350)
        self.sexe = sexe
        self.niv_nutrition = niv_nutrition

    def chasser(self, nb_proies, nb_coccinelles):
        '''
            Méthode prenant en paramètre 1 coccinelle de type Coccinelle,
            un nombre de proies nb_proies et un nombre de coccinelles nb_coccinelles
            Renvoie le nombre de proies qui reste après que la coccinelle ait consommé x proies
            Le nombre de consommation est calculé via des moyennes et du hasard en random
        '''
        # Si le nombre de coccinelles présentes pour chasser est nul, le nombre de poids reste tel quel
        if nb_coccinelles == 0:
            return nb_proies

        # On calcule le nombre de proies qui sera attribué par coccinelle
        proies_par_cocci = nb_proies / nb_coccinelles

        # On affecte un nombre de proies consommées selon le nombre de proies par coccinelles
        if proies_par_cocci > 20:
            consomme = random.randint(12, 20)
        elif proies_par_cocci > 10:
            consomme = random.randint(8, 15)
        else:
            consomme = random.randint(3, 8)

        # On affecte à consomme la valeur minimale entre une donnée hasardeuse (consomme elle-même) et le nombre de poids 
        consomme = min(consomme, nb_proies)

        # On gère le niveau de nutrition d'une coccinelle selon le nombre de proies consommées
        if consomme >= 10:
            self.niv_nutrition += 1
        else:
            self.niv_nutrition = max(0, self.niv_nutrition - 1)

        # On renvoie le nombre de proies qui reste après que notre coccinelle en ait consommé x
        return nb_proies - consomme

    def reproduction(self):
        """
        Une femelle avec un niveau de nutrition >= 2 engendre exactement
        deux descendants : un mâle et une femelle.
        """
        descendants = []
        # On ajoute self.age >= 20 puisque c'est à partir de 20 jours de vie
        if self.sexe == "femelle" and self.niv_nutrition >= 2 and self.age >= 20:
            descendants.append(Coccinelle("male", 0, 0))
            descendants.append(Coccinelle("femelle", 0, 0))
            self.niv_nutrition = 0

        return descendants

    def a_survecu(self):
        """
        Met à jour l'âge de la coccinelle et indique si elle est encore en vie.
        """
        # Si niv_nutrition est nulle, et que le hasard donne 3 (ici considérés comme mortel), on indique False
        if self.niv_nutrition == 0:
            if random.randint(1, 3) == 3:
                return False
        
        self.age = self.age + 1
        return self.age < self.esperance_de_vie

    def __repr__(self):
        return f"Coccinelle {self.sexe}, âge: {self.age}/{self.esperance_de_vie}, niv_nutrition: {self.niv_nutrition}"


def evolution(population, nb_proies):
    """
    Simule une journée dans l'écosystème :
    - chasse des coccinelles
    - reproduction
    - vieillissement et mortalité
    - croissance des pucerons

    population est une liste d'instances de la classe Coccinelle
    nb_proies est un entier indiquant le nombre de proies

    Cette fonction renvoie un couple (population_suivante, nouveau_nb_proies) indiquant
    la nouvelle population à la fin de la journée et le nombre de proies.
    """
    population_suivante = []
    nouveau_nes = []
    nb_coccinelles = len(population)

    for coccinelle in population:
        nb_proies = coccinelle.chasser(nb_proies, nb_coccinelles)

        if coccinelle.a_survecu():
            population_suivante.append(coccinelle)

        nouveau_nes += coccinelle.reproduction()

    # Croissance naturelle des pucerons (augmentation de 20% par jour)
    nb_proies = int(nb_proies * 1.2)

    # Ajout des nouveau-nés en fin de journée
    population_suivante += nouveau_nes

    return population_suivante, nb_proies


#############################################################################
# Écrire ci-dessous le code pour les questions de l'énoncé                  #
#############################################################################

def init_pop():
    a = Coccinelle("femelle", 10, 2)
    b = Coccinelle("femelle", 10, 2)
    c = Coccinelle("male", 10, 2)
    return [a, b, c]

def test_evolution():
    pop = init_pop()
    puc = 200
    for k in range(1, 6):
        pop, puc = evolution(pop, puc)
        print("Jour ", k," : \n Coccinelles : ", len(pop), " - Pucerons : ", puc, "\n")

def simulation_simple(population, nb_proies):
    for k in range(1, 31):
        population, nb_proies = evolution(population, nb_proies)
        res = (len(population), nb_proies, k)
        if len(population) == 0:
            print("Plus de coccinelles !")
            return res
        elif nb_proies == 0:
            print("Plus de pucerons !")
            return res
    return res
        
        
        
