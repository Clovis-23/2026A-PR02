from src.exceptions import Valeur_hors_norme, CategorieInvalide

class Variable():

    def __init__ (self, nom):
        self.nom=nom


class VariableIntervalles(Variable):
    def __init__(self, nom, minimum, maximum):
        super().__init__(nom)
        self.minimum= minimum
        self.maximum=maximum


    def valider(self, valeur):
        if valeur <self.minimum or valeur>self.maximum:
            raise Valeur_hors_norme("Valeur hors norme")
        return True
        
class VariableCategorielle(Variable):
    def __init__(self, nom,categories):
        super().__init__(nom)
        self.categories=categories
    
    def valider(self, valeur):
        if valeur not in  self.categories:
            raise CategorieInvalide(f"Cette valeur '{valeur}' n'appartient  pas à la categorie")
        return True

# vnum= VariableIntervalles("season_year", dictionnaire["intervalles"]["season_year"]["min"],dictionnaire["intervalles"]["season_year"]["max"])
# vnum.valider(joueur["season_year"])


        
